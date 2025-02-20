import streamlit as st
from firebase_config import db
from components.auth import get_current_user

def show():
    st.markdown("<h2 style='text-align: center;'>Complete Your Profile</h2>", unsafe_allow_html=True)
    
    user = get_current_user()
    if not user:
        st.error("❌ Please log in first.")
        return

    user_id = user.get("uid")
    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict() if user_ref.get().exists else {}

    # ✅ Industry-Standard Skills
    skill_options = [
        "Python", "Machine Learning", "Mathematics", "Data Science", "Cybersecurity", 
        "Cloud Computing", "Blockchain", "NLP", "DevOps", "Mobile App Dev", 
        "Full Stack Development", "Frontend Development", "Backend Development",
        "Software Testing", "Database Management", "Big Data", "Computer Vision", 
        "AI Ethics", "Robotics", "Digital Marketing", "UI/UX Design", "Product Management"
    ]

    # ✅ Include previously stored values in options if they are missing
    stored_skills = user_data.get("skills", [])
    for skill in stored_skills:
        if skill not in skill_options:
            skill_options.append(skill)  # Add missing skills dynamically

    selected_skills = st.multiselect("Your Skills", skill_options, default=stored_skills)
    custom_skill = st.text_input("Other Skill (if not listed)", "")
    if custom_skill:
        selected_skills.append(custom_skill)

    # ✅ Expanded Interests
    interest_options = [
        "AI", "Web Development", "Finance", "Cybersecurity", "Game Development", 
        "Data Engineering", "IoT", "Embedded Systems", "AR/VR", "Quantum Computing", 
        "HealthTech", "FinTech", "Bioinformatics", "Autonomous Vehicles", "E-commerce",
        "HR Tech", "Blockchain Applications", "Cloud Security", "Green Technology"
    ]

    stored_interests = user_data.get("interests", [])
    for interest in stored_interests:
        if interest not in interest_options:
            interest_options.append(interest)

    selected_interests = st.multiselect("Your Interests", interest_options, default=stored_interests)
    custom_interest = st.text_input("Other Interest (if not listed)", "")
    if custom_interest:
        selected_interests.append(custom_interest)

    # ✅ Learning Goals
    learning_goals = st.text_area("Your Learning Goal (e.g., Become an AI Engineer in 3 months)", user_data.get("learning_goals", ""))

    # ✅ Multiple Learning Styles
    learning_styles = ["Videos", "Text-based", "Hands-on Projects", "Podcasts", "Live Sessions", "Mentorship", "Bootcamps", "Online Courses"]
    
    stored_learning_styles = user_data.get("learning_style", [])
    for style in stored_learning_styles:
        if style not in learning_styles:
            learning_styles.append(style)

    selected_learning_styles = st.multiselect("Preferred Learning Style", learning_styles, default=stored_learning_styles)
    custom_learning_style = st.text_input("Other Learning Style (if not listed)", "")
    if custom_learning_style:
        selected_learning_styles.append(custom_learning_style)

    # ✅ Skip or Save
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Skip for Now"):
            st.session_state["profile_completed"] = True  # ✅ Mark as completed
            st.session_state["page"] = "dashboard"
            st.rerun()

    with col2:
        if st.button("Save Profile"):
            profile_data = {
                "skills": selected_skills,
                "interests": selected_interests,
                "learning_goals": learning_goals,
                "learning_style": selected_learning_styles
            }
            user_ref.set(profile_data, merge=True)  # ✅ Store data in Firebase
            st.success("✅ Profile updated successfully!")
            st.session_state["profile_completed"] = True
            st.session_state["page"] = "dashboard"
            st.rerun()
