from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CareerMemory:
    """
    Stores information generated during a CareerOps session.

    This is short-term application memory. It exists while the
    user is working on a career application and is not intended
    to be a permanent database.
    """

    # --------------------------------------------------------
    # Candidate information
    # --------------------------------------------------------

    cv_text: str = ""

    candidate_name: str = ""

    skills: List[str] = field(default_factory=list)

    experience: List[str] = field(default_factory=list)

    education: List[str] = field(default_factory=list)

    projects: List[str] = field(default_factory=list)


    # --------------------------------------------------------
    # Job information
    # --------------------------------------------------------

    job_description: str = ""

    job_title: str = ""

    company_name: str = ""


    # --------------------------------------------------------
    # Agent outputs
    # --------------------------------------------------------

    job_analysis: Dict[str, Any] = field(
        default_factory=dict
    )

    cv_analysis: Dict[str, Any] = field(
        default_factory=dict
    )

    company_research: Dict[str, Any] = field(
        default_factory=dict
    )

    application_materials: Dict[str, Any] = field(
        default_factory=dict
    )

    interview_preparation: Dict[str, Any] = field(
        default_factory=dict
    )

    critic_review: Dict[str, Any] = field(
        default_factory=dict
    )

    manager_summary: Dict[str, Any] = field(
        default_factory=dict
    )


    # --------------------------------------------------------
    # Workflow state
    # --------------------------------------------------------

    current_stage: str = "Not Started"

    workflow_status: str = "Not Started"

    revision_count: int = 0


    # --------------------------------------------------------
    # Errors / warnings
    # --------------------------------------------------------

    warnings: List[str] = field(
        default_factory=list
    )


    # --------------------------------------------------------
    # Update methods
    # --------------------------------------------------------

    def set_candidate_cv(self, cv_text: str):
        """Store the candidate's CV text."""

        self.cv_text = cv_text


    def set_job(
        self,
        job_description: str,
        job_title: str = "",
        company_name: str = ""
    ):
        """Store job information."""

        self.job_description = job_description
        self.job_title = job_title
        self.company_name = company_name


    def update_stage(self, stage: str):
        """Update the current workflow stage."""

        self.current_stage = stage


    def update_status(self, status: str):
        """Update overall workflow status."""

        self.workflow_status = status


    def add_warning(self, warning: str):
        """Add a warning to the session."""

        self.warnings.append(warning)


    def increment_revision(self):
        """Increase the revision counter."""

        self.revision_count += 1


    # --------------------------------------------------------
    # Agent result methods
    # --------------------------------------------------------

    def save_job_analysis(
        self,
        result: Dict[str, Any]
    ):
        self.job_analysis = result


    def save_cv_analysis(
        self,
        result: Dict[str, Any]
    ):
        self.cv_analysis = result


    def save_company_research(
        self,
        result: Dict[str, Any]
    ):
        self.company_research = result


    def save_application_materials(
        self,
        result: Dict[str, Any]
    ):
        self.application_materials = result


    def save_interview_preparation(
        self,
        result: Dict[str, Any]
    ):
        self.interview_preparation = result


    def save_critic_review(
        self,
        result: Dict[str, Any]
    ):
        self.critic_review = result


    def save_manager_summary(
        self,
        result: Dict[str, Any]
    ):
        self.manager_summary = result


    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(self):
        """
        Clear the current CareerOps session.
        """

        self.cv_text = ""

        self.candidate_name = ""

        self.skills.clear()

        self.experience.clear()

        self.education.clear()

        self.projects.clear()

        self.job_description = ""

        self.job_title = ""

        self.company_name = ""

        self.job_analysis.clear()

        self.cv_analysis.clear()

        self.company_research.clear()

        self.application_materials.clear()

        self.interview_preparation.clear()

        self.critic_review.clear()

        self.manager_summary.clear()

        self.current_stage = "Not Started"

        self.workflow_status = "Not Started"

        self.revision_count = 0

        self.warnings.clear()
