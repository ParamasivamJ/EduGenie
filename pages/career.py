import streamlit as st
import os
import requests
import pdfplumber  
from dotenv import load_dotenv
import speech_recognition as sr
import time

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Function to call Groq LLM API
def call_groq_llm(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "mixtral-8x7b-32768",  # Choose a model like Mixtral
                "messages": [{"role": "system", "content": "You're an AI Career Assistant."},
                             {"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 512
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {e}"

def show():
    st.title("🎓 AI-Powered Career Guidance")
    st.write("Helping you achieve your career goals with AI-powered tools.")

    # UI Containers
    st.subheader("🔧 Career Tools")
    tools = {
        "📍 Career Roadmap Generator": "roadmap",
        "📄 Resume Analyzer": "resume",
        "🎤 AI Mock Interview": "interview",
        "📝 Cover Letter Generator": "cover_letter",
        "🚀 AI Career Path Predictor": "career_path",
        "💼 Internship Finder": "internship"
    }
    selected_tool = st.selectbox("Select a tool", list(tools.keys()))

    # Career Roadmap Generator
    if selected_tool == "📍 Career Roadmap Generator":
        job_goal = st.text_input("Enter your career goal (e.g., Data Scientist, AI Engineer)")
        if st.button("Generate Roadmap"):
            roadmap_prompt = f"Generate a detailed step-by-step learning roadmap for becoming a {job_goal}."
            response = call_groq_llm(roadmap_prompt)
            st.write(response)

    # Resume Analyzer
    elif selected_tool == "📄 Resume Analyzer":
        resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
        if resume_file:
            try:
                resume_text = ""
                with pdfplumber.open(resume_file) as pdf:
                    for page in pdf.pages:
                        resume_text += page.extract_text() + "\n"

                resume_prompt = f"Analyze this resume and provide constructive feedback:\n{resume_text}"
                response = call_groq_llm(resume_prompt)
                st.write(response)
            except Exception as e:
                st.error(f"Error processing resume: {e}")

    # AI Mock Interviews (Now Speech-to-Speech Placeholder)
    def capture_speech():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🎤 Listening... Speak now! (You have up to 20 seconds)")

            recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise  
            try:
                audio = recognizer.listen(source, timeout=20, phrase_time_limit=20)  # Capture full response  
                response = recognizer.recognize_google(audio)
                return response
            except sr.WaitTimeoutError:
                return "❌ Timeout: No speech detected."
            except sr.UnknownValueError:
                return "❌ Could not understand audio."
            except sr.RequestError:
                return "❌ Speech Recognition API error."

    # AI Mock Interview Section
    if selected_tool == "🎤 AI Mock Interview":
        st.subheader("🎤 AI Mock Interview")

        # Get the job role
        role = st.text_input("Enter the job role for the interview (e.g., Data Scientist, AI Engineer)")
        
        if st.button("Start Interview"):
            if not role:
                st.error("Please enter a job role before starting.")
            else:
                st.write("⏳ Generating interview questions... Please wait...")
                
                # Ensure AI generates proper questions
                interview_prompt = f"Provide exactly 5 structured interview questions for an {role} position."
                ai_response = call_groq_llm(interview_prompt)

                # Extract only valid questions
                questions = [q.strip() for q in ai_response.split("\n") if q.strip() and q[0].isdigit()]
                
                if len(questions) < 5:
                    st.error("⚠️ AI did not generate enough questions. Try again.")
                else:
                    user_answers = []
                    
                    # Ask questions one by one
                    for i, question in enumerate(questions[:5]):
                        st.write(f"**Q{i+1}: {question}**")
                        time.sleep(1)
                        user_response = capture_speech()
                        
                        # If response is unclear, retry once
                        if "❌" in user_response:
                            st.write("⚠️ Speech unclear, please try again.")
                            user_response = capture_speech()
                        
                        user_answers.append((question, user_response))
                        st.write(f"🗣️ Your Answer: {user_response}")

                    # Generate feedback
                    feedback_prompt = "Evaluate the following interview responses and provide constructive feedback:\n"
                    for q, ans in user_answers:
                        feedback_prompt += f"Q: {q}\nA: {ans}\n\n"
                    
                    feedback = call_groq_llm(feedback_prompt)
                    st.subheader("📢 Interview Feedback")
                    st.write(feedback)

                    st.success("✅ Interview Completed! Keep practicing! 🎯")
    # Cover Letter Generator
    elif selected_tool == "📝 Cover Letter Generator":
        user_name = st.text_input("Your Name")
        user_email = st.text_input("Your Email")
        job_description = st.text_area("Paste the job description here")
        if st.button("Generate Cover Letter"):
            cover_letter_prompt = f"Write a professional cover letter for {user_name} applying to this job:\n{job_description}"
            response = call_groq_llm(cover_letter_prompt)
            st.write(response)

    # Career Path Predictor
    elif selected_tool == "🚀 AI Career Path Predictor":
        user_skills = st.text_area("Enter your skills (comma-separated)")
        if st.button("Predict Career Path"):
            career_prompt = f"Based on these skills, suggest the best career paths:\n{user_skills}"
            response = call_groq_llm(career_prompt)
            st.write(response)


    st.write("🚀 **Empowering your career with AI!**")

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "dashboard"
        st.rerun()




