import streamlit as st
from components.auth import signup_user

def show():
    st.markdown("<h2 style='text-align: center;'>Create an Account</h2>", unsafe_allow_html=True)

    full_name = st.text_input("Full Name")  # Add Full Name field
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        if full_name.strip() == "":  # Ensure name is provided
            st.error("❌ Full Name is required.")
        else:
            signup_user(email, password, full_name)  # Now passing full_name
    
    if st.button("Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()
