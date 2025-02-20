import streamlit as st
from firebase_config import db
from components.auth import get_current_user

def show():
    st.markdown("<h2 style='text-align: center;'>Your Profile</h2>", unsafe_allow_html=True)
    
    user = get_current_user()
    if not user:
        st.error("❌ Please log in first.")
        return

    user_id = user.get("uid")
    user_ref = db.collection("users").document(user_id)
    user_data = user_ref.get().to_dict() if user_ref.get().exists else {}

    # ✅ Display User Info
    st.write(f"**Full Name:** {user.get('full_name', 'Not Provided')}")
    st.write(f"**Email:** {user.get('email', 'Not Provided')}")
    st.write(f"**Skills:** {', '.join(user_data.get('skills', ['None']))}")
    st.write(f"**Interests:** {', '.join(user_data.get('interests', ['None']))}")
    st.write(f"**Learning Goals:** {user_data.get('learning_goals', 'Not Provided')}")
    st.write(f"**Preferred Learning Style:** {user_data.get('learning_style', 'Not Provided')}")

    if st.button("Edit Profile"):
        st.session_state["page"] = "user_profile"
        st.rerun()

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "dashboard"
        st.rerun()
