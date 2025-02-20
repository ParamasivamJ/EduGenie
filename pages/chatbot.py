import streamlit as st
from firebase_config import db
from models.chatbot import generate_response
import time

# UI
st.set_page_config(page_title="AI Tutor", layout="wide")
st.title("🎓 AI Tutor Chatbot")

# Get User Session
if "user" not in st.session_state:
    st.warning("⚠️ Please log in to use the chatbot.")
    st.stop()

user_id = st.session_state["user"]["localId"]
chat_ref = db.collection("chats").document(user_id)

# Load Chat History
chat_history = chat_ref.get().to_dict()
if chat_history:
    messages = chat_history.get("messages", [])
else:
    messages = []

# Chat Interface
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Input for User Query
user_query = st.chat_input("Ask a question...")
if user_query:
    # Store User Message
    messages.append({"role": "user", "text": user_query})
    
    # Get AI Response
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_query)
    
    # Store AI Response
    messages.append({"role": "assistant", "text": ai_response})
    
    # Update Firestore
    chat_ref.set({"messages": messages})

    # Display Messages
    with st.chat_message("user"):
        st.markdown(user_query)
    with st.chat_message("assistant"):
        st.markdown(ai_response)
