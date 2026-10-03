# --- Streamlit Cloud sqlite fix for Chroma (must run before chromadb import) ---
try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import pandas as pd
import streamlit as st

from agents import build_graph
from config import get_llm, get_secret
from rag import build_vectorstore, get_embeddings, load_uploaded_file, text_to_documents

st.set_page_config(page_title="CareerOp AI", page_icon="🧭", layout="wide")

NODE_LABELS = {
    "job_analyst": "Job Analyst: reading the job description",
    "cv_analyst": "CV Analyst: reading the CV",
    "match_score": "CV Analyst: calculating job match score",
    "skill_gap": "CV Analyst: detecting skill gaps",
    "matching_agent": "Matching Agent: comparing CV and job",
    "application_agent": "Application Agent: writing profile and cover letter",
    "manager_agent": "Manager Agent: building career roadmap",
    "reviewer": "Reviewer: checking everything",
}
IMPORTANCE_ICON = {"Critical": "🔴 Critical", "Important": "🟠 Important", "Nice-to-have": "🟡 Nice-to-have"}


@st.cache_resource(show_spinner="Loading embedding model...")
def cached_embeddings():
    return get_embeddings()


def score_label(score: int) -> str:
    if score >= 80:
        return "🟢 Strong match"
    if score >= 60:
        return "🟡 Good match, with gaps"
    if score >= 40:
        return "🟠 Partial match"
    return "🔴 Weak match"


def build_report(r: dict) -> str:
    ms = r.get("match_score", {})
    gaps = r.get("skill_gaps", {}).get("gaps", [])
    gap_lines = "\n".join(
        f"- {g.get('skill')} ({g.get('status')}, {g.get('importance')})" for g in gaps
    ) or "None identified."
    return f"""# CareerOp AI Report

## Job Match Score: {ms.get('overall', 'n/a')}%
{ms.get('verdict', '')}

## Skill Gaps
{gap_lines}

## Cover Letter
{r.get('cover_letter', '')}

## Career Roadmap
{r.get('roadmap', '')}

## Application Materials
{r.get('application', '')}

## Matching Analysis
{r.get('matching', '')}

## Reviewer Feedback
{r.get('review', '')}
"""


# ------------------------------- Sidebar -------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    provider = str(get_secret("LLM_PROVIDER", "gemini")).lower()
    key_name = "GROQ_API_KEY" if provider == "groq" else "GOOGLE_API_KEY"
    user_key = None
    if not get_secret(key_name):
        user_key = st.text_input(f"{key_name}", type="password",
                                 help="Not stored. Or add it to Streamlit secrets.")

    st.subheader("Cover letter")
    tone = st.selectbox("Tone", ["Professional and warm", "Formal", "Confident and direct",
                                 "Enthusiastic and friendly"])
    company = st.text_input("Company name (optional)")
    hiring_manager = st.text_input("Hiring manager (optional)")

    st.subheader("Career roadmap")
    roadmap_days = st.select_slider("Timeframe (days)", options=[30, 60, 90, 180], value=90)
    hours_per_week = st.slider("Study hours per week", 2, 30, 8)

# ------------------------------- Inputs -------------------------------
st.title("🧭 CareerOp AI: Personal Operations Team")
st.caption("Upload a CV and a job description. Your AI team scores the match, finds skill gaps, "
           "writes a cover letter and builds a career roadmap.")

col1, col2 = st.columns(2)
with col1:
    cv_file = st.file_uploader("Candidate CV", type=["pdf", "txt"], key="cv")
    cv_text = st.text_area("...or paste CV text", height=120)
with col2:
    job_file = st.file_uploader("Job description", type=["pdf", "txt"], key="job")
    job_text = st.text_area("...or paste job description", height=120)

run = st.button("🚀 Run AI Team", type="primary", use_container_width=True)

# ------------------------------- Run pipeline -------------------------------
if run:
    cv_docs = load_uploaded_file(cv_file, "CV") if cv_file else text_to_documents(cv_text, "CV", "cv_text")
    job_docs = (load_uploaded_file(job_file, "JOB_DESCRIPTION") if job_file
                else text_to_documents(job_text, "JOB_DESCRIPTION", "job_text"))

    if not cv_docs or not job_docs:
        st.error("Please provide both a CV and a job description (upload or paste).")
        st.stop()
    if not (user_key or get_secret(key_name)):
        st.error(f"Missing {key_name}.")
        st.stop()

    results = {}
    try:
        with st.status("AI team is working...", expanded=True) as status:
            st.write("Indexing documents (chunk, embed, store)...")
            vs = build_vectorstore(cv_docs + job_docs, cached_embeddings())
            graph = build_graph(
                get_llm(api_key=user_key),
                vs,
                {
                    "tone": tone.lower(),
                    "company": company,
                    "hiring_manager": hiring_manager,
                    "roadmap_days": roadmap_days,
                    "hours_per_week": hours_per_week,
                },
            )
            for step in graph.stream({"job_analysis": ""}, stream_mode="updates"):
                for node, update in step.items():
                    results.update(update)
                    st.write(f"✅ {NODE_LABELS.get(node, node)}")
            status.update(label="Done! Your results are ready below.", state="complete", expanded=False)
        st.session_state["results"] = results
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.stop()

# ------------------------------- Results -------------------------------
r = st.session_state.get("results")
if r:
    ms = r["match_score"]
    gaps = r["skill_gaps"]["gaps"]

    tab_score, tab_gaps, tab_letter, tab_road, tab_more = st.tabs(
        ["🎯 Match Score", "🧩 Skill Gaps", "✉️ Cover Letter", "🗺️ Career Roadmap", "📋 Details & Review"]
    )

    with tab_score:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Job Match Score", f"{ms['overall']}%")
            st.progress(ms["overall"] / 100)
            st.write(score_label(ms["overall"]))
        with c2:
            st.write(ms["verdict"])
            labels = {"technical_skills": "Technical skills (40%)", "experience": "Experience (30%)",
                      "education": "Education (10%)", "keywords_soft_skills": "Keywords & soft skills (20%)"}
            for k, label in labels.items():
                st.write(f"{label}: **{ms['breakdown'][k]}%**")
                st.progress(ms["breakdown"][k] / 100)
        s1, s2 = st.columns(2)
        with s1:
            st.subheader("✅ Why you match")
            for s in ms["strengths"]:
                st.markdown(f"**{s.get('point', '')}**  \n_Evidence: {s.get('evidence', '')}_")
        with s2:
            st.subheader("⚠️ Why the score isn't higher")
            for w in ms["weaknesses"]:
                st.markdown(f"**{w.get('point', '')}**  \n_{w.get('evidence', '')}_")

    with tab_gaps:
        strong = r["skill_gaps"]["strong_skills"]
        if strong:
            st.success("Skills you already show: " + ", ".join(strong))
        if gaps:
            df = pd.DataFrame([{
                "Skill": g.get("skill"),
                "Status": g.get("status"),
                "Importance": IMPORTANCE_ICON.get(g.get("importance"), g.get("importance")),
                "What the job asks": g.get("job_evidence"),
                "What your CV shows": g.get("cv_evidence"),
            } for g in gaps])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No significant skill gaps were detected.")

    with tab_letter:
        letter = st.text_area("Edit your cover letter", r["cover_letter"], height=420)
        st.download_button("⬇️ Download cover letter (.txt)", letter, "cover_letter.txt")

    with tab_road:
        st.markdown(r["roadmap"])
        st.download_button("⬇️ Download roadmap (.md)", r["roadmap"], "career_roadmap.md")

    with tab_more:
        with st.expander("Job analysis"):
            st.markdown(r["job_analysis"])
        with st.expander("CV analysis"):
            st.markdown(r["cv_analysis"])
        with st.expander("Matching analysis"):
            st.markdown(r["matching"])
        with st.expander("Application materials (profile, CV improvements, keywords)"):
            st.markdown(r["application"])
        with st.expander("Reviewer feedback", expanded=True):
            st.markdown(r["review"])
        with st.expander("Retrieved evidence (RAG)"):
            for label, key in [("CV", "cv_evidence"), ("Job description", "job_evidence")]:
                st.markdown(f"**{label}**")
                for e in r.get(key, []):
                    st.caption(f"{e['file']} · page {e['page']}")
                    st.text(e["text"][:500])
        st.download_button("⬇️ Download full report (.md)", build_report(r), "careerop_report.md")
