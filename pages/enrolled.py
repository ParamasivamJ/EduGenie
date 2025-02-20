import streamlit as st
from firebase_config import db
from components.auth import get_current_user

# 🔹 Function to fetch enrolled courses
def fetch_enrolled_courses(user_id):
    """Retrieve the user's enrolled courses from Firestore."""
    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict()
    
    return user_data.get("enrolled_courses", [])

# 🔹 Function to save course progress
def update_course_progress(user_id, course_index, module_index):
    """Mark a module as completed for a course."""
    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict()

    enrolled_courses = user_data.get("enrolled_courses", [])
    
    if course_index < len(enrolled_courses):
        course = enrolled_courses[course_index]
        
        if "progress" not in course:
            course["progress"] = []

        if module_index not in course["progress"]:
            course["progress"].append(module_index)
        
        enrolled_courses[course_index] = course
        user_ref.update({"enrolled_courses": enrolled_courses})

# 🔹 Function to unenroll from a course
def unenroll_course(user_id, course_index):
    """Remove a course from the enrolled courses list."""
    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict()
    
    enrolled_courses = user_data.get("enrolled_courses", [])

    if course_index < len(enrolled_courses):
        del enrolled_courses[course_index]
        user_ref.update({"enrolled_courses": enrolled_courses})

# 🔹 Streamlit UI for Learning Dashboard
def show():
    st.markdown("<h2 style='text-align: center;'>🎓 Your Learning Dashboard</h2>", unsafe_allow_html=True)

    # Get current user
    user = get_current_user()
    if not user:
        st.error("❌ Please log in first.")
        st.stop()

    user_id = user.get("uid")

    # Fetch user's enrolled courses
    enrolled_courses = fetch_enrolled_courses(user_id)

    if not enrolled_courses:
        st.warning("📌 You haven't enrolled in any courses yet.")
        st.stop()

    # Display each enrolled course
    for course_index, course in enumerate(enrolled_courses):
        with st.expander(f"📚 {course['title']}"):
            st.write(f"**Domain:** {course['domain']}")
            
            # Track course progress
            progress = course.get("progress", [])
            total_modules = len(course.get("LearningPath", {}))
            completed_modules = len(progress)
            progress_percentage = (completed_modules / total_modules) * 100 if total_modules else 0

            st.progress(progress_percentage / 100)

            # Display modules
            for module_index, (module_title, module_details) in enumerate(course.get("LearningPath", {}).items()):
                completed = module_index in progress
                checkbox = st.checkbox(f"✅ {module_title}", value=completed, key=f"{course_index}_{module_index}")
                
                if checkbox and not completed:
                    update_course_progress(user_id, course_index, module_index)
                    st.experimental_rerun()

            # Option to Unenroll
            if st.button("❌ Unenroll", key=f"unenroll_{course_index}"):
                unenroll_course(user_id, course_index)
                st.experimental_rerun()
    
    st.button("🔙 Back to Dashboard", on_click=lambda: st.session_state.update({"page": "dashboard"}))
