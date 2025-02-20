import streamlit as st
import requests
import json
import time
import os
from dotenv import load_dotenv
from firebase_config import db  
from components.auth import get_current_user  
import ast 
# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ Groq API Key is missing. Check your .env file.")
    st.stop()

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
    """Extracts JSON content safely, even if the format has errors."""
    try:
        # ✅ Clean JSON response from Markdown artifacts
        response_text = response_text.strip().replace("```json", "").replace("```", "").strip()

        # ✅ Try loading as JSON directly
        return json.loads(response_text)
    
    except json.JSONDecodeError as e:
        try:
            # ✅ Attempt to fix structural issues
            corrected_text = response_text.replace("\n", "").replace("\t", "").strip()
            return json.loads(corrected_text)
        
        except json.JSONDecodeError:
            return {"error": f"Invalid JSON format: {str(e)}", "raw_response": response_text}


# 🔹 Function to generate a structured learning pathway
def generate_learning_pathway(selected_domain, extra_prompt=""):
    """Creates a structured learning roadmap using AI."""
    
    prompt = f"""
    Generate a structured and personalized learning pathway for a user interested in {selected_domain} and {extra_prompt}.

    ### Learning Path Structure:
    1️⃣ **Introduction & Fundamentals**  
       - List the core foundational topics required for {selected_domain} and {extra_prompt} 
       - Provide a short explanation of why each topic is important  
       - Suggest high-quality **free resources** (courses, books, or articles)  

    2️⃣ **Core Concepts & Practical Applications**  
       - Define the key subtopics to master in  {selected_domain} and {extra_prompt} 
       - Include **hands-on projects** and exercises for each module  
       - Link to **completely free and industry-standard resources**  

    3️⃣ **Advanced Topics & Specializations**  
       - Provide an advanced learning path based on the user's goal domain  {selected_domain} and {extra_prompt}
       - Recommend real-world case studies and projects  

    4️⃣ **Certifications & Industry Recognition**  
       - List **free certification programs** from trusted platforms (AWS, Google, Harvard, MIT, etc.)  in  {selected_domain} and {extra_prompt}
       - Provide details on how to earn and leverage these certifications  

    5️⃣ **Real-World Projects & Portfolio Building**  for domain {selected_domain} and {extra_prompt}
       - Suggest **free open-source projects**, Kaggle challenges, and GitHub repositories  
       - Provide resources for building a strong **portfolio**  

    6️⃣ **Community & Continuous Learning**  
       - List relevant forums, newsletters, and conferences  
       - Recommend **top YouTube channels, podcasts, and blogs** in  {selected_domain} and {extra_prompt}

    ### Requirements:
    - **All resources must be 100% free and from trusted sources** (official company websites, universities, or top-tier open resources).
    - Provide the response in **valid JSON format**.
    """

    response_data = call_groq_api(prompt)

    if "error" in response_data:
        return response_data  

    return extract_json_from_response(response_data["choices"][0]["message"]["content"])

# 🔹 Function to save enrolled courses to Firebase
def enroll_course(user_id, learning_pathway):
    """Enrolls the user in a course and saves it in Firestore."""
    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict() or {}  # Ensure user_data is a dictionary

    # 🔹 Ensure "enrolled_courses" exists in Firestore
    enrolled_courses = user_data.get("enrolled_courses", [])  # If missing, set to an empty list

    # 🔹 Prevent duplicate enrollments
    if any(course["title"] == learning_pathway.get("title") for course in enrolled_courses):
        st.warning("⚠️ You are already enrolled in this course!")
        return

    # 🔹 Append the new course
    enrolled_courses.append({
        "title": learning_pathway.get("title", "Unknown Course"),
        "domain": learning_pathway.get("domain", "Unknown Domain"),
        "LearningPath": learning_pathway.get("LearningPath", {}),
        "progress": []  # Initialize progress tracking
    })

    # 🔹 Update Firestore
    user_ref.set({"enrolled_courses": enrolled_courses}, merge=True)  # 🔥 Use `merge=True` to keep other fields

    st.success("🎉 Successfully enrolled in the course!")


# 🔹 Streamlit UI
# 🔹 Streamlit UI
def show():
    st.markdown("<h2 style='text-align: center;'>🚀 AI-Powered Learning Pathway</h2>", unsafe_allow_html=True)

    # Get current user
    user = get_current_user()
    if not user:
        st.error("❌ Please log in first.")
        st.stop()

    user_id = user.get("uid")

    # User selects a domain or topic
    st.subheader("📌 Select Your Learning Topic")
    domain_options = [
        "Artificial Intelligence", "Data Science", "Cybersecurity", "Software Development", 
        "Blockchain", "Cloud Computing", "UI/UX Design", "Digital Marketing", "Product Management"
    ]
    selected_domain = st.selectbox("Choose a topic:", domain_options)
    
    # Option for custom domain
    custom_domain = st.text_input("Other Skill (if not listed)", "")
    if custom_domain:
        selected_domain = custom_domain

    # Option to customize the course before generation
    extra_prompt = st.text_input("🎯 Want specific content? Add your request here!")

    # Generate learning pathway
    if st.button("🚀 Generate Learning Pathway"):
        with st.spinner("Generating your personalized learning pathway..."):
            learning_pathway = generate_learning_pathway(selected_domain, extra_prompt)
            # Debugging: Print full response to check structure
            st.write("### Generated Learning pathway!")
            st.json(learning_pathway)  # Display raw JSON for debugging

           

                # Option to modify before enrolling
            if st.button("✏️ Modify Course"):
                    st.experimental_rerun()  # Allows the user to go back and choose another course

                # Option to enroll in the generated course
            if st.button("✅ Enroll in Course"):
                    enroll_course(user_id, learning_pathway)
                    st.success("🎉 You are now enrolled in this course! Check your 'Enrolled Courses' page.")

    st.button("🔙 Back to Dashboard", on_click=lambda: st.session_state.update({"page": "dashboard"}))

