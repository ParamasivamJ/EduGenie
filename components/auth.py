import streamlit as st
import firebase_admin
from firebase_admin import auth, firestore
from firebase_config import db, auth_pyrebase  # Import Firestore config

def check_auth():
    """Check if user is logged in by looking at session state."""
    return st.session_state.get("user", None)

def login_user(email, password):
    """Authenticate user and fetch details from Firestore."""
    try:
        user = auth_pyrebase.sign_in_with_email_and_password(email, password)  # Authenticate with Firebase
        user_id = user["localId"]
        user_info = auth.get_user_by_email(email)  # Fetch user info

        # Fetch user details from Firestore
        user_doc = db.collection("users").document(user_info.uid).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            user_data["uid"] = user_id
            st.session_state["user"] = user_data
            st.session_state["page"] = "dashboard"
            st.rerun()
        else:
            st.error("❌ User record not found in database.")

    except Exception as e:
        error_message = str(e)

        if "INVALID_PASSWORD" in error_message:
            st.error("❌ Incorrect password. Try again.")
        elif "EMAIL_NOT_FOUND" in error_message:
            st.error("❌ No account found with this email. Sign up first.")
        else:
            st.error(f"❌ Login failed: Enter valid Credentials")

def signup_user(email, password, full_name):
    """Register a new user and store details in Firestore."""
    try:
        # Create user in Firebase Authentication
        user = auth.create_user(email=email, password=password)

        # Store user info in Firestore
        user_data = {
            "uid": user.uid,
            "full_name": full_name,
            "email": email,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        db.collection("users").document(user.uid).set(user_data)

        st.success("✅ Account created successfully! Please log in.")
        st.session_state["page"] = "login"
        st.rerun()

    except Exception as e:
        error_message = str(e)

        # Handle common Firebase errors
        if "EMAIL_EXISTS" in error_message:
            st.error("❌ Email already in use. Try logging in.")
        elif "WEAK_PASSWORD" in error_message:
            st.error("❌ Password must be at least 6 characters long.")
        else:
            st.error(f"❌ Signup failed: {error_message}")

def get_current_user():
    """Retrieve the current logged-in user's data from session state."""
    return st.session_state.get("user", None)


def redirect_to(page):
    """Redirect user to a different page using session state."""
    st.session_state["page"] = page
    st.rerun()
