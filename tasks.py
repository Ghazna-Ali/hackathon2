from crewai import Task

from agents import (
    manager_agent,
    job_analyst_agent,
    cv_agent,
    research_agent,
    application_agent,
    interview_agent,
    critic_agent,
)


# ============================================================
# MANAGER TASK
# ============================================================

manager_task = Task(
    description="""
Analyze the user's career situation.

CAREER REQUEST:
{career_request}

JOB DESCRIPTION:
{job_description}

CANDIDATE CV:
{cv_text}

Provide:
1. Career goal analysis
2. Important job requirements
3. Candidate strengths
4. Potential gaps
5. Recommended next steps

Use only the information provided.
Do not invent candidate qualifications or experience.
""",
    expected_output="""
A structured career analysis covering the career goal,
job requirements, candidate strengths, gaps, and
recommended next steps.
""",
    agent=manager_agent,
)


# ============================================================
# JOB ANALYST TASK
# ============================================================

job_analysis_task = Task(
    description="""
Analyze this job description.

JOB DESCRIPTION:
{job_description}

CAREER REQUEST:
{career_request}

Identify:
1. Job title
2. Responsibilities
3. Required qualifications
4. Preferred qualifications
5. Technical skills
6. Soft skills
7. Education requirements
8. Experience requirements
9. Tools and technologies
10. Certifications
11. Important keywords

Do not invent requirements.
""",
    expected_output="""
A structured job analysis containing responsibilities,
required and preferred qualifications, skills, experience,
education, technologies, certifications, and keywords.
""",
    agent=job_analyst_agent,
)


# ============================================================
# CV ANALYST TASK
# ============================================================

cv_analysis_task = Task(
    description="""
Analyze the candidate's CV against the target job.

CANDIDATE CV:
{cv_text}

JOB DESCRIPTION:
{job_description}

CAREER REQUEST:
{career_request}

Identify:
1. Candidate skills
2. Education
3. Experience
4. Projects
5. Certifications
6. Relevant achievements
7. Strong matches
8. Missing requirements
9. Weak areas
10. CV improvements

Only use information contained in the CV.
Never invent qualifications or experience.
""",
    expected_output="""
A structured CV-to-job analysis containing candidate
strengths, relevant evidence, missing requirements,
weak areas, and recommended CV improvements.
""",
    agent=cv_agent,
)


# ============================================================
# RESEARCH TASK
# ============================================================

company_research_task = Task(
    description="""
Analyze the company and job opportunity using only the
information provided by the user.

JOB DESCRIPTION:
{job_description}

CAREER REQUEST:
{career_request}

CANDIDATE CV:
{cv_text}

Provide:
1. Company information available in the input
2. Industry/context
3. Role context
4. Important themes
5. Potential company priorities
6. Suggested areas for further research
7. Interview preparation topics

IMPORTANT:
You do not have live web access.
Do not claim that you searched the internet.
Do not invent company facts.
""",
    expected_output="""
A factual company and opportunity analysis based only
on the supplied information.
""",
    agent=research_agent,
)


# ============================================================
# APPLICATION TASK
# ============================================================

application_task = Task(
    description="""
Create tailored application guidance.

CANDIDATE CV:
{cv_text}

JOB DESCRIPTION:
{job_description}

CAREER REQUEST:
{career_request}

Provide:
1. Professional summary
2. CV improvement recommendations
3. Important keywords
4. Improved bullet suggestions
5. Cover letter guidance
6. Application strategy
7. Suggested application answers

Everything must be truthful and based on the supplied
candidate information.

Do not invent experience, achievements, qualifications,
skills, projects, or certifications.
""",
    expected_output="""
A professional application package containing a
professional summary, CV recommendations, keywords,
application strategy, and cover-letter guidance.
""",
    agent=application_agent,
)


# ============================================================
# INTERVIEW TASK
# ============================================================

interview_task = Task(
    description="""
Prepare the candidate for an interview.

CANDIDATE CV:
{cv_text}

JOB DESCRIPTION:
{job_description}

CAREER REQUEST:
{career_request}

Create:
1. Technical questions
2. Behavioral questions
3. Situational questions
4. Job-specific questions
5. CV-based questions
6. Questions about potential gaps
7. Answer frameworks
8. STAR guidance where appropriate
9. Topics to revise
10. Questions for the interviewer

Keep all suggested answers truthful.
""",
    expected_output="""
A complete interview preparation guide containing
technical, behavioral, situational, job-specific,
and CV-based questions with preparation guidance.
""",
    agent=interview_agent,
)


# ============================================================
# CRITIC TASK
# ============================================================

critic_task = Task(
    description="""
Review the candidate's application information.

CANDIDATE CV:
{cv_text}

JOB DESCRIPTION:
{job_description}

CAREER REQUEST:
{career_request}

Identify:
1. Missing requirements
2. Weak candidate evidence
3. CV weaknesses
4. Generic application content
5. Unsupported claims
6. Missing keywords
7. Interview preparation gaps
8. Potential inconsistencies
9. Areas requiring clarification
10. Specific improvements

Do not invent candidate or company information.
""",
    expected_output="""
A detailed quality review identifying application
weaknesses, evidence gaps, missing requirements,
interview gaps, and specific improvements.
""",
    agent=critic_agent,
)


# ============================================================
# TASK REGISTRY
# ============================================================

TASKS = {
    "Manager": manager_task,
    "Job Analyst": job_analysis_task,
    "CV Analyst": cv_analysis_task,
    "Research Agent": company_research_task,
    "Application Agent": application_task,
    "Interview Agent": interview_task,
    "Critic Agent": critic_task,
}
