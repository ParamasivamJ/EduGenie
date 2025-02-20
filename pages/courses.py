import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from models.recommender import generate_recommendations

# Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/firebase-config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("📚 AI-Based Course Recommendations")

# Fetch user courses from Firebase
user_id = st.session_state.get("user_id")
if not user_id:
    st.error("Please log in to view courses.")
    st.stop()

saved_courses = db.collection("courses").where("user_id", "==", user_id).stream()
saved_courses = [doc.to_dict()["course_name"] for doc in saved_courses]

# Show saved courses
if saved_courses:
    st.subheader("Your Enrolled Courses")
    for course in saved_courses:
        st.write(f"✅ {course}")

    # Generate recommendations using AI
    recommended_courses = generate_recommendations(saved_courses)
    if recommended_courses:
        st.subheader("🔮 Recommended Courses for You")
        for rec in recommended_courses:
            st.markdown(f"**{rec['name']}** - {rec['description']}")
else:
    st.warning("You haven't enrolled in any courses yet.")

# Course Enrollment
new_course = st.text_input("Search for a new course")
if st.button("Enroll"):
    if new_course:
        db.collection("courses").add({"user_id": user_id, "course_name": new_course})
        st.success(f"Enrolled in {new_course}!")
