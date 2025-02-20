import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.header("📌 Navigation")
        st.page_link("pages/dashboard.py", label="🏠 Dashboard")
        st.page_link("pages/courses.py", label="📖 Courses")
        st.page_link("pages/quiz.py", label="📝 Quizzes")
        st.page_link("pages/chatbot.py", label="🤖 AI Tutor")
        st.page_link("pages/analytics.py", label="📊 Analytics")
        st.page_link("pages/gamification.py", label="🏆 Gamification")
        st.page_link("pages/settings.py", label="⚙️ Settings")

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.switch_page("pages/login.py")
