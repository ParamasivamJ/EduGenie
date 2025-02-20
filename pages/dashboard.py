import streamlit as st

def show():
    st.markdown("<h1 style='text-align: center;'>Student Dashboard</h1>", unsafe_allow_html=True)

    if st.button("View Profile"):
        st.session_state["page"] = "profile"
        st.rerun()
    # Sidebar Navigation
    st.sidebar.header("📌 Navigation")

    if st.sidebar.button("📚 Courses"):
        st.session_state["page"] = "learning_pathway"
        st.rerun()

    if st.sidebar.button("🤖 AI Chatbot"):
        st.session_state["page"] = "chatbot"
        st.rerun()

    if st.sidebar.button("Enrolled Courses"):
        st.session_state["page"] = "enrolled"
        st.rerun()
    
    if st.sidebar.button("🎓 Career Guidance"):
        st.session_state["page"] = "career"
        st.rerun()
        

    # Logout button in sidebar
    if st.sidebar.button("🔄 Logout"):
        st.session_state.pop("user", None)
        st.session_state["page"] = "home"  # Redirect to home after logout
        st.rerun()
