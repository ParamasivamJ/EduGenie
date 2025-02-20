import streamlit as st
import requests
import json
import time
import os
from dotenv import load_dotenv
from firebase_config import db  
from components.auth import get_current_user  

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Ensure API keys are available
if not GROQ_API_KEY:
    st.error("❌ Groq API Key is missing. Check your .env file.")

# 🔹 Function to call Groq API with retry logic
def call_groq_api(prompt):
    """Handles API call with retry mechanism."""
    max_retries = 3  
    delay = 2  

    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={"model": "mixtral-8x7b-32768", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7},
                timeout=30  
            )

            if response.status_code == 200:
                return response.json()  

            time.sleep(delay)

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    return {"error": "Failed after multiple attempts"}

# 🔹 Function to extract JSON response properly
def extract_json_from_response(response_text):
    """Extracts JSON content from API response."""
    try:
        if response_text.startswith("json\n"):
            response_text = response_text[5:].strip()
        elif response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        
        return json.loads(response_text)  
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format: {str(e)}", "raw_response": response_text}

# 🔹 Function to generate a learning pathway using Groq API
def generate_learning_pathway(user_data, extra_prompt=""):
    """Generates a structured learning pathway using AI."""
    
    prompt = f"""
    Generate a structured learning pathway for a user interested in {user_data['selected_domain']}.

    User Profile:
    - Skills: {', '.join(user_data['skills'])}
    - Interests: {', '.join(user_data['interests'])}
    - Learning Style: {', '.join(user_data['learning_style'])}
    - Learning Goal: {user_data['learning_goals']}
    - Additional Request: {extra_prompt}

    The pathway should follow this structure:
    1. Introduction & Orientation
    2. Beginner Module (Concepts, Quizzes, Hands-on Exercises)
    3. Intermediate Module (Case Studies, Real-world Applications, Projects)
    4. Advanced Module (Specialized Topics, Capstone Project, Mentorship)
    5. Completion & Career Guidance (Certification, Portfolio, Job Prep)

    Ensure the roadmap is structured, engaging, and provides interactive elements.

    Format the response in **valid JSON** with section names, descriptions, and at least 3 recommended learning resources with **valid URLs**.
    """

    response_data = call_groq_api(prompt)

    if "error" in response_data:
        return response_data  

    return extract_json_from_response(response_data["choices"][0]["message"]["content"])


# 🔹 Function to save enrolled courses to Firebase
def enroll_course(user_id, learning_pathway):
    """Enrolls the user in a course and saves it in Firestore."""
    user_ref = db.collection("users").document(user_id)
    
    user_data = user_ref.get().to_dict()
    enrolled_courses = user_data.get("enrolled_courses", [])

    enrolled_courses.append(learning_pathway)  
    user_ref.update({"enrolled_courses": enrolled_courses})

    return True

# 🔹 Streamlit UI
def show():
    st.markdown("<h2 style='text-align: center;'>🚀 AI-Powered Learning Pathway</h2>", unsafe_allow_html=True)

    # Get current user
    user = get_current_user()
    if not user:
        st.error("❌ Please log in first.")
        return

    user_id = user.get("uid")

    # Pre-fill user data
    user_data = {
        "skills": user.get("skills", ["Not specified"]),
        "interests": user.get("interests", ["Not specified"]),
        "learning_goals": user.get("learning_goals", "Not specified"),
        "learning_style": user.get("learning_style", ["Not specified"])
    }

    # User selects domain or topic
    st.subheader("📌 Select Your Domain")
    domain_options = [
        "Artificial Intelligence", "Data Science", "Cybersecurity", "Software Development", 
        "Blockchain", "Cloud Computing", "UI/UX Design", "Digital Marketing", "Product Management"
    ]
    selected_domain = st.selectbox("Choose a domain:", domain_options)
    user_data["selected_domain"] = selected_domain

    # Allow user to customize inputs
    skills = st.multiselect("Your Skills", user_data["skills"], default=user_data["skills"])
    interests = st.multiselect("Your Interests", user_data["interests"], default=user_data["interests"])
    learning_goals = st.text_area("Your Learning Goal", user_data["learning_goals"])
    learning_style = st.multiselect("Preferred Learning Style", user_data["learning_style"], default=user_data["learning_style"])

    # Option to add extra prompts for customization
    extra_prompt = st.text_input("Want to customize your course? Add specific requests here!")

    # Generate learning pathway
    if st.button("Generate Learning Pathway"):
        user_data.update({"skills": skills, "interests": interests, "learning_goals": learning_goals, "learning_style": learning_style})

        with st.spinner("Generating your personalized learning pathway..."):
            learning_pathway = generate_learning_pathway(user_data, extra_prompt)
            
            if "error" in learning_pathway:
                st.error("❌ Failed to generate learning pathway. Please try again.")
            else:
                st.success("✅ Learning pathway generated!")

                # Display AI-generated learning pathway
                st.write("### 📚 Your Personalized Learning Pathway:")
                st.json(learning_pathway)  

                if st.button("✅ Enroll in Course"):
                    enroll_course(user_id, learning_pathway)
                    st.success("🎉 You are now enrolled in this course! Check your 'Enrolled Courses' page.")

    st.button("🔙 Back to Dashboard", on_click=lambda: st.session_state.update({"page": "dashboard"}))
