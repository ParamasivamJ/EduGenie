from firebase_config import auth, db
import streamlit as st

# Function to Sign Up New Users
def signup(email, password, name):
    if len(password) < 6:
        st.error("⚠️ Password must be at least 6 characters long!")
        return None

    try:
        user = auth.create_user_with_email_and_password(email, password)
        uid = user["localId"]
        db.collection("users").document(uid).set({"name": name, "email": email})

        # Send Email Verification
        auth.send_email_verification(user['idToken'])

        st.success("✅ Account created successfully! Please check your email for verification.")
        return user
    except Exception as e:
        error_message = str(e)
        if "WEAK_PASSWORD" in error_message:
            st.error("⚠️ Password is too weak! Use at least 6 characters.")
        elif "EMAIL_EXISTS" in error_message:
            st.error("⚠️ This email is already registered. Try logging in.")
        elif "INVALID_EMAIL" in error_message:
            st.error("⚠️ Please enter a valid email address.")
        else:
            st.error(f"Signup Error: {e}")

# Function to Log In Existing Users
def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        
        # Check if email is verified
        user_info = auth.get_account_info(user['idToken'])
        if not user_info['users'][0]['emailVerified']:
            st.error("⚠️ Please verify your email before logging in.")
            return None
        
        st.success("✅ Login successful!")
        st.session_state["user"] = user  # Store in session
        return user
    except Exception as e:
        error_message = str(e)
        if "INVALID_LOGIN_CREDENTIALS" in error_message:
            st.error("⚠️ Incorrect email or password. Please try again.")
        elif "TOO_MANY_ATTEMPTS" in error_message:
            st.error("⚠️ Too many failed attempts. Try again later.")
        else:
            st.error(f"Login Error: {e}")

# Function to Log Out Users
def logout():
    st.session_state["user"] = None
    st.success("✅ Logged out successfully!")
