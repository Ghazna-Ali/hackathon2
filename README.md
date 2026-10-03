# 🤖 Career Assistant AI

**Career Assistant AI** is a Gemini-powered, multi-agent AI career assistant designed to help job seekers analyze opportunities, improve their CVs, research companies, prepare applications, practice interviews, and identify weaknesses in their career materials.

Built with **Python, Streamlit, Google Gemini, and specialized AI agents**, the application provides users with direct control over which career task they want the AI to perform.

Instead of automatically running every agent, users can **select the specialized agent they need**, provide their career information, and receive a focused AI-generated analysis.

At the end of each workflow, the generated result can also be turned into a **downloadable career report**.

---

## 🌟 Overview

Searching and applying for jobs often requires completing several different tasks:

* Understanding complex job descriptions
* Identifying required skills and keywords
* Comparing a CV with a target position
* Finding missing qualifications or experience
* Researching a company and opportunity
* Writing tailored application content
* Preparing for technical and behavioral interviews
* Reviewing an application for weaknesses
* Organizing all of this information into useful reports

**Career Assistant AI** brings these tasks together into one Streamlit-based application.

The application provides multiple specialized AI agents, each designed for a particular stage of the career and job-application process.

### Core workflow

```text
                 ┌──────────────────────┐
                 │      Streamlit       │
                 │     User Interface   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Select AI Agent    │
                 └──────────┬───────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
     Job Analyst        CV Analyst       Research Agent
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   Application Agent   Interview Agent   Critic Agent
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Gemini API   │
                    └───────┬───────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │  AI Generated      │
                  │  Career Analysis   │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │  Download Report   │
                  └────────────────────┘
```

---

# 🚀 Features

## 1. 🎯 User-Controlled AI Agents

Career Assistant AI provides specialized agents for different career tasks.

Users select the agent they want to use rather than being forced through a predefined workflow.

### Available agents

| Agent                    | Purpose                                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| 🧭 **Manager**           | Provides a structured overview of the user's career situation, job requirements, strengths, gaps, and next steps |
| 💼 **Job Analyst**       | Analyzes job descriptions, requirements, skills, keywords, responsibilities, and qualifications                  |
| 📄 **CV Analyst**        | Compares a CV against a target job and identifies matches, gaps, and improvement opportunities                   |
| 🏢 **Research Agent**    | Analyzes company and opportunity information provided by the user                                                |
| ✍️ **Application Agent** | Creates tailored application guidance, professional summaries, CV improvements, and cover-letter content         |
| 🎤 **Interview Agent**   | Generates technical, behavioral, situational, and job-specific interview preparation                             |
| 🔎 **Critic Agent**      | Reviews application information and identifies weaknesses, missing evidence, gaps, and potential improvements    |

---

# 🧠 Agent Details

## 🧭 Manager Agent

The Manager agent provides a broader career overview.

It can help organize information around:

* Current career situation
* Target role
* Job requirements
* Existing strengths
* Skill gaps
* Areas requiring improvement
* Potential next steps

It acts as a high-level career analysis assistant.

---

## 💼 Job Analyst Agent

The Job Analyst focuses specifically on the target job description.

It can analyze:

* Job title
* Required qualifications
* Preferred qualifications
* Technical skills
* Soft skills
* Responsibilities
* Keywords
* Experience requirements
* Education requirements
* Tools and technologies
* Important role expectations

The goal is to turn an often lengthy job description into a structured understanding of what the employer is looking for.

### Example output areas

```text
Job Overview
Required Skills
Preferred Skills
Key Responsibilities
Important Keywords
Experience Requirements
Qualifications
Potential Candidate Priorities
```

---

## 📄 CV Analyst Agent

The CV Analyst compares the user's CV with a target job.

It can identify:

* Matching skills
* Relevant experience
* Missing skills
* Missing keywords
* Qualification gaps
* Weak CV sections
* Opportunities for stronger wording
* Areas that could be better aligned with the target role

The purpose is not simply to summarize the CV, but to analyze its relevance to a specific opportunity.

### Example workflow

```text
CV
 │
 ▼
Extract Skills & Experience
 │
 ▼
Compare Against Job Requirements
 │
 ├── Matches
 ├── Gaps
 ├── Missing Keywords
 └── Improvement Opportunities
 │
 ▼
CV Improvement Recommendations
```

---

## 🏢 Research Agent

The Research Agent focuses on company and opportunity information supplied by the user.

It can help structure and analyze:

* Company information
* Opportunity context
* Role characteristics
* Organization-related information
* Potential areas the candidate should investigate
* Questions or considerations before applying

The agent works with the information provided through the user's career request and job description.

---

## ✍️ Application Agent

The Application Agent helps transform career information into application-ready content.

It can assist with:

* Professional summaries
* CV improvement suggestions
* Tailored application guidance
* Job-specific positioning
* Cover-letter content
* Highlighting relevant experience
* Presenting skills more effectively

A typical workflow is:

```text
Candidate Information
        +
Job Description
        │
        ▼
Application Agent
        │
        ├── Professional Summary
        ├── CV Improvements
        ├── Relevant Experience
        └── Cover Letter Content
```

---

## 🎤 Interview Agent

The Interview Agent helps candidates prepare for interviews based on their target role.

It can generate:

### Technical questions

Questions related to:

* Role-specific technical knowledge
* Tools
* Technologies
* Concepts
* Practical scenarios

### Behavioral questions

Examples involving:

* Teamwork
* Leadership
* Communication
* Conflict
* Adaptability
* Problem solving

### Situational questions

Role-specific hypothetical scenarios designed to help the candidate practice decision-making and communication.

### Job-specific preparation

The agent can use the supplied job description and candidate information to make preparation more relevant to the target position.

---

## 🔎 Critic Agent

The Critic Agent acts as a review layer.

It looks for potential weaknesses in the information provided by the candidate.

It can identify:

* Missing evidence
* Skill gaps
* Weak descriptions
* Missing qualifications
* Inconsistencies
* Areas lacking specificity
* Weak application content
* Opportunities for improvement

The purpose is to encourage another review before the candidate uses their application materials.

---

# 🔄 How Career Assistant AI Works

Career Assistant AI follows a **selective-agent architecture**.

Unlike a system where every agent automatically executes in sequence, the user decides which specialized agent to use.

### Step 1 — Open the application

The application is deployed through Streamlit.

The interface provides the user with access to the available career agents.

---

### Step 2 — Select an agent

The user chooses the task they want help with.

For example:

```text
Agent:
[ Job Analyst ▼ ]
```

Other options include:

```text
Manager
Job Analyst
CV Analyst
Research Agent
Application Agent
Interview Agent
Critic Agent
```

---

### Step 3 — Provide career information

Depending on the selected task, the user provides relevant information such as:

* Job description
* CV
* Career background
* Skills
* Experience
* Company information
* Target role
* Interview context

---

### Step 4 — Execute the selected agent

Only the selected agent is executed.

For example:

```text
User selects:
Job Analyst

        ↓

Job Analyst receives the input

        ↓

Gemini API processes the request

        ↓

Job analysis is generated
```

The other agents are not unnecessarily executed.

This makes the workflow more direct and user-controlled.

---

### Step 5 — Display the result

The AI-generated analysis is displayed inside the Streamlit application.

The user can review the generated information and recommendations.

---

### Step 6 — Generate a downloadable report

After the analysis is generated, Career Assistant AI provides the result in a downloadable report format.

This allows users to retain the generated career analysis rather than relying only on the temporary Streamlit session.

```text
AI Analysis
     │
     ▼
Report Generation
     │
     ▼
Download
     │
     ▼
Career Report
```

---

# 🏗️ Architecture

The application is built around several main components.

```text
┌─────────────────────────────────────────┐
│              Streamlit UI               │
│                                         │
│  Agent Selection                        │
│  User Input                             │
│  Results                                │
│  Report Download                        │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│             Agent Selection             │
│                                         │
│ Manager                                  │
│ Job Analyst                              │
│ CV Analyst                               │
│ Research Agent                           │
│ Application Agent                        │
│ Interview Agent                          │
│ Critic Agent                             │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│              Agent Logic                │
│                                         │
│ Prompts / Tasks / Specialized Analysis  │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│             Google Gemini               │
│               API                       │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│          Generated AI Response          │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│           Report Generation             │
│                                         │
│        Downloadable Career Report       │
└─────────────────────────────────────────┘
```

---

# 🧩 Project Structure

The project is organized into separate Python modules for the application, agents, tasks, tools, and memory.

```text
Career-Assistant-AI/
│
├── app.py
├── agents.py
├── tasks.py
├── tools.py
├── memory.py
├── requirements.txt
└── README.md
```

## `app.py`

The main Streamlit application.

Responsible for:

* User interface
* Agent selection
* User input
* Calling the selected agent
* Displaying results
* Report download functionality
* Application state

---

## `agents.py`

Contains the specialized AI agent definitions.

The agents include:

```text
Manager
Job Analyst
CV Analyst
Research Agent
Application Agent
Interview Agent
Critic Agent
```

Each agent is configured for a specific career-related purpose.

---

## `tasks.py`

Contains task definitions and instructions used by the agents.

Tasks help translate the user's request into structured AI work.

---

## `tools.py`

Contains supporting tools used by the application and agents.

This allows functionality to be separated from the main application and agent definitions.

---

## `memory.py`

Provides memory-related functionality for the career workflow.

It can be used to maintain relevant information across parts of the career-assistance workflow.

---

## `requirements.txt`

Contains the Python dependencies required to run the application.

---

# 🛠️ Technology Stack

| Technology               | Purpose                             |
| ------------------------ | ----------------------------------- |
| **Python**               | Core programming language           |
| **Streamlit**            | Web application and user interface  |
| **Google Gemini API**    | Generative AI capabilities          |
| **CrewAI**               | Agent/task-oriented AI architecture |
| **GitHub**               | Source code and version control     |
| **Streamlit Deployment** | Application hosting                 |

---

# 🔐 Gemini API Configuration

Career Assistant AI uses the **Google Gemini API** to generate AI-powered career analysis.

The application requires a Gemini API key.

The application can detect whether the required Gemini API configuration is available.

Example application status:

```text
System Status

Gemini API key detected
```

The API key should be stored securely and should **not be hard-coded into the source code or committed to GitHub**.

For local development, environment variables or Streamlit secrets should be used.

---

# 💻 Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/sizzlingish/CareerOp-AI.git
```

Move into the project directory:

```bash
cd CareerOp-AI
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure the Gemini API key

Set your Gemini API key using an environment variable or Streamlit secrets.

For example, using an environment variable:

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

### macOS / Linux

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Alternatively, configure the secret through Streamlit's secrets management when deploying the application.

**Never commit your API key to GitHub.**

---

## 5. Run the application

Start Streamlit with:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ☁️ Deployment

Career Assistant AI can be deployed using **Streamlit's deployment platform**.

A typical deployment flow is:

```text
GitHub Repository
       │
       ▼
Streamlit Deployment
       │
       ▼
Configure Secrets
       │
       ▼
Gemini API Key
       │
       ▼
Running Career Assistant AI
```

### Deployment requirements

The repository should contain:

```text
app.py
requirements.txt
agents.py
tasks.py
tools.py
memory.py
```

The Gemini API key should be configured through the deployment platform's secrets/settings rather than committed to the repository.

---

# 📋 Example Use Cases

## Use Case 1 — Analyze a Job

A user finds a job posting and wants to understand what the employer is looking for.

They select:

```text
Job Analyst
```

Then provide the job description.

The agent can return:

```text
Job Overview
Required Skills
Preferred Skills
Responsibilities
Keywords
Qualifications
Experience Requirements
```

The user can then download the resulting report.

---

## Use Case 2 — Evaluate a CV

A candidate has a CV and wants to compare it with a specific position.

They select:

```text
CV Analyst
```

Then provide:

```text
CV + Job Description
```

The agent analyzes the relationship between the candidate's background and the target role.

---

## Use Case 3 — Prepare an Application

A candidate wants help tailoring their application.

They select:

```text
Application Agent
```

The agent can provide:

* Professional summary
* CV improvement suggestions
* Relevant experience positioning
* Application guidance
* Cover-letter content

---

## Use Case 4 — Prepare for an Interview

A candidate has an upcoming interview.

They select:

```text
Interview Agent
```

The system can generate role-specific:

* Technical questions
* Behavioral questions
* Situational questions
* Preparation guidance
* Questions to consider asking during the interview

---

## Use Case 5 — Critique an Application

A candidate wants another review before submitting an application.

They select:

```text
Critic Agent
```

The agent can identify:

* Missing evidence
* Weak sections
* Skill gaps
* Missing information
* Areas that could be strengthened

---

# 📊 Example End-to-End Workflow

A complete job-search workflow could look like:

```text
                Job Description
                       │
                       ▼
                ┌──────────────┐
                │ Job Analyst  │
                └──────┬───────┘
                       │
                       ▼
              Understand Requirements
                       │
                       ▼
                 ┌────────────┐
                 │ CV Analyst │
                 └─────┬──────┘
                       │
                       ▼
                 Identify CV Gaps
                       │
                       ▼
              ┌─────────────────┐
              │ Application     │
              │ Agent           │
              └────────┬────────┘
                       │
                       ▼
                Improve Application
                       │
                       ▼
              ┌─────────────────┐
              │ Critic Agent    │
              └────────┬────────┘
                       │
                       ▼
                 Review Weaknesses
                       │
                       ▼
              ┌─────────────────┐
              │ Interview Agent │
              └────────┬────────┘
                       │
                       ▼
                 Prepare for Interview
                       │
                       ▼
                Download Reports
```

**Important:** These are separate user-selected workflows. Career Assistant AI does not automatically execute all of these agents as one mandatory pipeline. The user chooses which agent to run at each stage.

---

# 🎨 User Interface

The Streamlit interface is designed around a simple interaction model:

```text
⚙️ Career Assistant AI

Agent
[ Select an agent ]

        ↓

Career / Job Information

        ↓

[ Run Agent ]

        ↓

AI Generated Analysis

        ↓

[ Download Report ]
```

The interface also displays system status information, including whether the Gemini API configuration has been detected.

---

# 🔒 Security Considerations

Career Assistant AI may process sensitive career information such as:

* CVs
* Employment history
* Skills
* Education
* Job applications
* Career goals
* Company information

Users should therefore avoid exposing sensitive information unnecessarily.

### API key security

Never store API keys directly in:

```python
# ❌ Do not do this
GEMINI_API_KEY = "my-secret-api-key"
```

Instead, use environment variables or secure deployment secrets.

### GitHub security

Before pushing code to GitHub, ensure that secrets are not included in:

* Python files
* `.env` files
* Configuration files
* Notebooks
* Logs
* Commit history

---

# ⚠️ Limitations

Career Assistant AI is an AI-powered assistance tool and its outputs should be reviewed by the user.

AI-generated recommendations may contain:

* Incorrect interpretations
* Missing context
* Inaccurate assumptions
* Overly general recommendations
* Incorrectly inferred relationships between skills and job requirements

The system should therefore be used as a **career assistance and preparation tool**, rather than as a replacement for the user's own judgment.

The quality of the output also depends on the quality and completeness of the information provided to the selected agent.

---

# 🔮 Future Improvements

Potential future development areas include:

* 📄 Direct CV file upload and parsing
* 📊 CV-to-job compatibility scoring
* 🔍 Automated job-search integration
* 🌐 Live company research
* 📝 Export to PDF/DOCX
* 📚 Persistent user career profiles
* 🧠 Improved long-term career memory
* 🎯 Personalized career roadmaps
* 📈 Application tracking
* 🔔 Job application reminders
* 🎤 Interactive interview simulation
* 💬 Follow-up interview conversations
* 🔄 Multi-agent collaborative workflows
* 📊 Application history and analytics
* 🌍 Support for multiple languages

---

# 🧪 Development Philosophy

Career Assistant AI follows a modular architecture.

Instead of putting all career functionality into a single large AI prompt, the application separates responsibilities into specialized agents.

```text
One General AI
      │
      │
      ▼
Specialized Career Agents
      │
      ├── Job Analysis
      ├── CV Analysis
      ├── Research
      ├── Applications
      ├── Interviews
      ├── Criticism
      └── Career Overview
```

This separation makes it easier to:

* Maintain the application
* Improve individual agents
* Add new career capabilities
* Modify prompts independently
* Debug specific workflows
* Give users direct control over the task being performed

---

# 📈 Project Goals

The main goals of Career Assistant AI are to:

1. Simplify the job-search process.
2. Help candidates understand job requirements.
3. Improve alignment between CVs and job descriptions.
4. Assist with tailored application materials.
5. Help candidates prepare for interviews.
6. Identify weaknesses before applications are submitted.
7. Provide structured, reusable career reports.
8. Give users control over which AI capability they want to use.

---

# 🏆 Why Career Assistant AI?

Traditional job applications require candidates to manually switch between many different tools.

For example:

```text
Job Description
      ↓
Manual Analysis
      ↓
CV Editing
      ↓
Company Research
      ↓
Cover Letter
      ↓
Interview Preparation
      ↓
Manual Review
```

Career Assistant AI brings these capabilities into a single application:

```text
             Career Assistant AI
                     │
       ┌─────────────┼──────────────┐
       │             │              │
    Analyze         Improve       Prepare
       │             │              │
       ▼             ▼              ▼
     Jobs           CVs         Interviews
       │             │              │
       └─────────────┼──────────────┘
                     ▼
              Review & Report
```

The user remains in control of which capability to use.

---

# 🧑‍💻 Development

Contributions and improvements are welcome.

A typical development process is:

```text
Fork / Clone
     ↓
Create Feature
     ↓
Test Locally
     ↓
Run Streamlit
     ↓
Commit Changes
     ↓
Push to GitHub
     ↓
Deploy
```

When adding a new agent, consider:

1. Define the agent's purpose.
2. Create its specialized instructions.
3. Add the agent to the available agent selection.
4. Define the corresponding task.
5. Test the generated output.
6. Integrate report generation where appropriate.
7. Update the README.

---

# 📄 License

Add the project's chosen license here.

If no license has been selected yet, this section should be updated before distributing the project as open-source software.

---

# 👨‍💻 Project

**Career Assistant AI**

An AI-powered career assistance platform built with:

* 🐍 Python
* 🎨 Streamlit
* 🤖 Google Gemini
* 🧩 Specialized AI Agents
* 🔗 CrewAI
* ☁️ Streamlit Deployment

---

## ⭐ Summary

**Career Assistant AI** provides a centralized AI-powered workspace for career analysis and job-application preparation.

Users can select a specialized agent based on their current need:

```text
Manager
Job Analyst
CV Analyst
Research Agent
Application Agent
Interview Agent
Critic Agent
```

The selected agent processes the user's career information through the Gemini API and produces a focused result. The result can then be converted into a **downloadable report**, giving the user a reusable record of the analysis.

The architecture is modular, user-controlled, and designed to make AI-assisted career preparation more structured and accessible.
