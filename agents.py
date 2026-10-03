"""Agents + LangGraph workflow.

Flow:
START -> Job Analyst -> CV Analyst -> Job Match Score -> Skill Gap Detector
      -> Matching Agent -> Application Agent (profile + cover letter)
      -> Manager Agent (career roadmap) -> Reviewer -> END
"""
import json
import re
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

import prompts as P
from rag import retrieve

SCORE_WEIGHTS = {
    "technical_skills": 0.40,
    "experience": 0.30,
    "education": 0.10,
    "keywords_soft_skills": 0.20,
}


class TeamState(TypedDict, total=False):
    job_analysis: str
    cv_analysis: str
    job_evidence: list
    cv_evidence: list
    match_score: dict
    skill_gaps: dict
    matching: str
    application: str
    cover_letter: str
    roadmap: str
    review: str


def _text(response) -> str:
    content = response.content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return content


def _parse_json(raw: str) -> dict | None:
    raw = re.sub(r"```(?:json)?", "", raw).strip()
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(raw[start:end + 1])
    except json.JSONDecodeError:
        return None


def _clamp(value, low=0, high=100) -> int:
    try:
        return max(low, min(high, int(round(float(value)))))
    except (TypeError, ValueError):
        return 0


def _fmt(items: list[dict], key: str = "point") -> str:
    return "\n".join(f"- {i.get(key, '')}" for i in items) or "None identified."


class CareerTeam:
    def __init__(self, llm, vectorstore, options: dict | None = None):
        self.llm = llm
        self.vs = vectorstore
        self.opt = {
            "tone": "professional and warm",
            "company": "",
            "hiring_manager": "",
            "roadmap_days": 90,
            "hours_per_week": 8,
            **(options or {}),
        }

    # ---------- helpers ----------
    def _ask(self, prompt: str) -> str:
        return _text(self.llm.invoke(prompt))

    def _ask_json(self, prompt: str) -> dict:
        raw = self._ask(prompt)
        data = _parse_json(raw)
        if data is None:  # one retry with a stricter nudge
            raw = self._ask(prompt + "\n\nYour last answer was not valid JSON. Return ONLY the JSON object.")
            data = _parse_json(raw)
        return data or {}

    # ---------- agents ----------
    def job_analyst(self, state: TeamState) -> dict:
        ctx, ev = retrieve(self.vs, "job title requirements skills responsibilities qualifications",
                           "JOB_DESCRIPTION", k=6)
        return {"job_analysis": self._ask(P.fill(P.JOB_ANALYST, CONTEXT=ctx)), "job_evidence": ev}

    def cv_analyst(self, state: TeamState) -> dict:
        ctx, ev = retrieve(self.vs, "education skills projects experience certifications achievements",
                           "CV", k=6)
        return {"cv_analysis": self._ask(P.fill(P.CV_ANALYST, CONTEXT=ctx)), "cv_evidence": ev}

    def _cv_raw(self) -> str:
        ctx, _ = retrieve(self.vs, "skills tools technologies projects experience", "CV", k=8)
        return ctx

    def match_score(self, state: TeamState) -> dict:
        """NEW (CV Analyst): percentage match with reasons."""
        data = self._ask_json(P.fill(
            P.MATCH_SCORE,
            JOB=state["job_analysis"], CV=state["cv_analysis"], CV_RAW=self._cv_raw(),
        ))
        breakdown = {k: _clamp(data.get("breakdown", {}).get(k, 0)) for k in SCORE_WEIGHTS}
        overall = _clamp(sum(breakdown[k] * w for k, w in SCORE_WEIGHTS.items()))
        return {"match_score": {
            "overall": overall,
            "breakdown": breakdown,
            "verdict": data.get("verdict", "Score could not be fully explained."),
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
        }}

    def skill_gap(self, state: TeamState) -> dict:
        """NEW (CV Analyst): missing / weak skills for this job."""
        data = self._ask_json(P.fill(
            P.SKILL_GAP,
            JOB=state["job_analysis"], CV=state["cv_analysis"], CV_RAW=self._cv_raw(),
        ))
        order = {"Critical": 0, "Important": 1, "Nice-to-have": 2}
        gaps = sorted(data.get("gaps", []), key=lambda g: order.get(g.get("importance"), 3))
        return {"skill_gaps": {"gaps": gaps, "strong_skills": data.get("strong_skills", [])}}

    def matching_agent(self, state: TeamState) -> dict:
        return {"matching": self._ask(P.fill(P.MATCHING, JOB=state["job_analysis"], CV=state["cv_analysis"]))}

    def application_agent(self, state: TeamState) -> dict:
        """Profile + CV improvements, and NEW: customized cover letter."""
        gaps = state["skill_gaps"]["gaps"]
        gap_text = ", ".join(g.get("skill", "") for g in gaps) or "None identified."
        strengths = _fmt(state["match_score"]["strengths"])

        application = self._ask(P.fill(P.APPLICATION_PROFILE, MATCHING=state["matching"], GAPS=gap_text))
        cover_letter = self._ask(P.fill(
            P.COVER_LETTER,
            JOB=state["job_analysis"], CV=state["cv_analysis"],
            STRENGTHS=strengths, GAPS=gap_text,
            COMPANY=self.opt["company"] or "Not provided",
            MANAGER=self.opt["hiring_manager"] or "Not provided",
            TONE=self.opt["tone"],
        ))
        return {"application": application, "cover_letter": cover_letter}

    def manager_agent(self, state: TeamState) -> dict:
        """NEW (Manager Agent): learning / career roadmap from all team reports."""
        gaps = state["skill_gaps"]
        roadmap = self._ask(P.fill(
            P.CAREER_ROADMAP,
            JOB=state["job_analysis"], CV=state["cv_analysis"],
            SCORE=state["match_score"]["overall"],
            GAPS=json.dumps(gaps["gaps"], indent=1),
            STRONG=", ".join(gaps["strong_skills"]) or "None identified.",
            DAYS=self.opt["roadmap_days"], HOURS=self.opt["hours_per_week"],
        ))
        return {"roadmap": roadmap}

    def reviewer(self, state: TeamState) -> dict:
        return {"review": self._ask(P.fill(
            P.REVIEWER,
            CV=state["cv_analysis"], APPLICATION=state["application"],
            COVER_LETTER=state["cover_letter"], ROADMAP=state["roadmap"],
        ))}


def build_graph(llm, vectorstore, options: dict | None = None):
    team = CareerTeam(llm, vectorstore, options)
    g = StateGraph(TeamState)
    steps = [
        ("job_analyst", team.job_analyst),
        ("cv_analyst", team.cv_analyst),
        ("match_score", team.match_score),
        ("skill_gap", team.skill_gap),
        ("matching_agent", team.matching_agent),
        ("application_agent", team.application_agent),
        ("manager_agent", team.manager_agent),
        ("reviewer", team.reviewer),
    ]
    for name, fn in steps:
        g.add_node(name, fn)
    g.add_edge(START, steps[0][0])
    for (a, _), (b, _) in zip(steps, steps[1:]):
        g.add_edge(a, b)
    g.add_edge(steps[-1][0], END)
    return g.compile()
