import streamlit as st

# ✅ Ensure this is the first command in the script
st.set_page_config(page_title="AI Education Platform", layout="wide")

from components.auth import check_auth
import pages.home as home
import pages.dashboard as dashboard
import pages.login as login  
import pages.signup as signup 
import pages.career as career  
import pages.user_profile as user_profile  
import pages.profile as profile
import pages.learning_pathway as learning_pathway
import pages.enrolled as enrolled
# Remove default sidebar UI
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# ✅ Check if the user is authenticated
user = check_auth()

# ✅ If user is logged in, check if they have completed their profile
if user:
    if "profile_completed" not in st.session_state:
        st.session_state["profile_completed"] = False  # Default to False

    # ✅ If profile is not completed, redirect to User Profile Page
    if not st.session_state["profile_completed"]:
        user_profile.show()
    else:
        # ✅ Navigate to the appropriate page
        if st.session_state["page"] == "dashboard":
            dashboard.show()
        elif st.session_state["page"] == "career":
            career.show()
        elif st.session_state["page"] == "profile":
            profile.show()
        elif st.session_state["page"] == "learning_pathway":
            learning_pathway.show()
        elif st.session_state["page"] == "enrolled":
            enrolled.show()
        else:
            st.session_state["page"] = "dashboard"
            st.rerun()
else:
    # ✅ If not authenticated, show login/signup pages
    if st.session_state["page"] == "home":
        home.show()
    elif st.session_state["page"] == "login":
        login.show()
    elif st.session_state["page"] == "signup":
        signup.show()
