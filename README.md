# 🤖 AI Interview Practice App (CrewAI + Gemini)

An AI-powered interview preparation web app built using **Streamlit**, **CrewAI Agents**, and **Google Gemini LLM**.  
It helps users generate interview questions, answer them, and receive detailed AI-based evaluation including score, feedback, and ideal answers.

---

## 🚀 Features

- Upload Resume (**PDF / TXT**)
- Generate interview questions:
  - HR Questions
  - Technical Questions (Role-based)
  - Behavioral Questions (STAR Method)
  - Resume-Based Questions (Personalized)
- Answer directly in the app
- Get AI evaluation with:
  - Score (1–10)
  - Strengths
  - Weaknesses
  - Improvements
  - Perfect example answer

---

## 🛠️ Tech Stack

- Python
- Streamlit
- CrewAI
- Google Gemini API
- PyPDF2
- python-dotenv

---

## 📂 Project Structure

```bash
AI-Interview-Practice/
│── app.py
│── requirements.txt
│── .env
│── README.md
c

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/ai-interview-practice.git
cd ai-interview-practice
```
### 2️⃣ Create Virtual Environment
```bash 
python -m venv venv
```
Activate the environment:
Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
## 🔑 Setup Gemini API Key

- Create a `.env` file in the project folder and add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```
### ▶️ Run the App
```bash
streamlit run app.py
```

