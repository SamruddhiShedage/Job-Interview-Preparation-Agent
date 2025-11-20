import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai import LLM
import os
import PyPDF2

# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ GEMINI_API_KEY missing in .env file! Add it to .env")
    st.stop()

# ---------------------------------------------------------
# Streamlit Setup
# ---------------------------------------------------------
st.set_page_config(page_title="AI Interview Practice", layout="wide")
st.title("🤖 AI Interview Practice (CrewAI + Gemini)")
st.write("Upload resume → generate interview questions → answer → get evaluation")

# ---------------------------------------------------------
# Resume Upload
# ---------------------------------------------------------
resume_file = st.file_uploader("📄 Upload Resume (PDF/TXT)", type=["pdf", "txt"])
resume_text = ""

if resume_file:
    if resume_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(resume_file)
        for page in reader.pages:
            resume_text += page.extract_text() + "\n"
    else:
        resume_text = resume_file.read().decode("utf-8")

    st.success("Resume uploaded successfully!")

role = st.text_input("🎯 Job Role (for Technical Questions)")
category = st.selectbox("Select Question Type", ["HR", "Technical", "Behavioral", "Resume-Based"])

# ---------------------------------------------------------
# Gemini LLM
# ---------------------------------------------------------
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=API_KEY
)

# ---------------------------------------------------------
# Agents
# ---------------------------------------------------------
question_agent = Agent(
    role="Interview Question Generator",
    goal="Generate smart and relevant interview questions.",
    backstory="Expert HR and technical interviewer.",
    llm=gemini_llm,
    allow_delegation=False
)

evaluation_agent = Agent(
    role="Answer Evaluator",
    goal="Evaluate answers with improvements.",
    backstory="Expert interview evaluator.",
    llm=gemini_llm,
    allow_delegation=False
)

resume_agent = Agent(
    role="Resume Analyzer",
    goal="Generate questions based on resume.",
    backstory="Expert resume analyst.",
    llm=gemini_llm,
    allow_delegation=False
)

# ---------------------------------------------------------
# Generate Question
# ---------------------------------------------------------
if st.button("Generate Interview Question"):

    if category == "Resume-Based" and not resume_text.strip():
        st.error("Upload a resume first!")
        st.stop()

    if category == "Technical" and not role.strip():
        st.error("Enter a job role!")
        st.stop()

    # Build prompt
    if category == "HR":
        prompt = "Generate a professional HR interview question."

    elif category == "Technical":
        prompt = f"Generate a technical interview question for job role: {role}"

    elif category == "Behavioral":
        prompt = "Generate a behavioral interview question using the STAR method."

    else:
        prompt = f"Generate one personalized interview question from this resume:\n\n{resume_text}"

    task = Task(
        description=prompt,
        agent=question_agent,
        expected_output="A single interview question."
    )

    crew = Crew(agents=[question_agent], tasks=[task])
    result = crew.kickoff()

    # Extract clean question
    try:
        question = result.tasks_output[0].raw
    except:
        question = result.raw

    st.session_state["question"] = question

    st.subheader("📝 Generated Question")
    st.write(question)

# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------
if "question" in st.session_state:

    user_answer = st.text_area("✍️ Your Answer:")

    if st.button("Evaluate Answer"):

        if not user_answer.strip():
            st.error("Write your answer first!")
            st.stop()

        eval_prompt = f"""
Evaluate this interview answer.

QUESTION: {st.session_state['question']}
ANSWER: {user_answer}

Provide:
• Score (1–10)
• Strengths
• Weaknesses
• Improvements
• A perfect example answer
"""

        eval_task = Task(
            description=eval_prompt,
            agent=evaluation_agent,
            expected_output="Evaluation + improved answer"
        )

        eval_crew = Crew(agents=[evaluation_agent], tasks=[eval_task])
        result = eval_crew.kickoff()

        try:
            evaluation = result.tasks_output[0].raw
        except:
            evaluation = result.raw

        st.subheader("📊 Evaluation")
        st.write(evaluation)
