import streamlit as st
from PIL import Image

# Load and resize the logo
image = Image.open("assets/logo.png")  
image = image.resize((150, 150))  # Adjust size as needed

def show():
    # Hide Streamlit's default sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    # Center the title
    st.markdown("<h1 style='text-align: center;'>Welcome to AI Education Platform</h1>", unsafe_allow_html=True)
    

    # Centered text
    st.markdown(
        "<p style='text-align: center; font-size:18px;'>🚀 AI-powered learning platform with adaptive courses, quizzes, and gamification.</p>", 
        unsafe_allow_html=True
    )

    # Centered buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:  # Centered column for buttons
        login_btn = st.button("🔑 Login", use_container_width=True)
        signup_btn = st.button("📝 Signup", use_container_width=True)

    # Handle button clicks with session state navigation
    if login_btn:
        st.session_state.page = "login"
        st.rerun()

    if signup_btn:
        st.session_state.page = "signup"
        st.rerun()
