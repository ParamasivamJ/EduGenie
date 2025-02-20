import streamlit as st
from components.auth import login_user

def show():
    st.markdown("<h2 style='text-align: center;'>Login to AI Education</h2>", unsafe_allow_html=True)
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        login_user(email, password)
    
    if st.button("Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()
