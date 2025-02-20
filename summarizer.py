import os
import json
import streamlit as st
import requests
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Load Hugging Face API key from .env
load_dotenv()
HF_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

# Hugging Face API headers
HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# Set Streamlit page config
st.set_page_config(page_title="AI Chatbot Summarizer", page_icon="🤖", layout="wide")

# UI Header
st.title("🤖 AI-Powered Summarizer Chatbot")
st.write("Summarize YouTube videos, PDFs, and chat with AI to get insights.")

# Sidebar for Features
with st.sidebar:
    st.image("https://source.unsplash.com/400x200/?education,ai", use_column_width=True)
    st.markdown("### Features:")
    st.markdown("✔️ Summarize YouTube transcripts")
    st.markdown("✔️ Summarize PDFs and images")
    st.markdown("✔️ Chatbot for Q&A")
    st.markdown("✔️ Instant AI-powered insights")

# Function to fetch summary from Hugging Face API
def fetch_summary(text):
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    payload = json.dumps({
        "inputs": text, 
        "parameters": {"max_length": 250}  # Set max_length for better summarization
    })
    response = requests.post(api_url, headers=HF_HEADERS, data=payload)

    if response.status_code == 200:
        try:
            return response.json()[0]['summary_text']
        except (KeyError, IndexError):
            return "Error: Unexpected response format"
    
    return f"Error: {response.status_code} - {response.text}"

# Function to fetch answer from Hugging Face API
def fetch_answer(question, context):
    api_url = "https://api-inference.huggingface.co/models/impira/layoutlm-document-qa"
    payload = json.dumps({
        "inputs": {
            "question": question, 
            "context": context
        }
    })
    
    response = requests.post(api_url, headers=HF_HEADERS, data=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            answer = data.get('answer', 'No answer found.')
            score = data.get('score', 0)
            
            if score > 0.3:  # Ensure confidence threshold
                return answer
            return "I'm not sure. This may be outside the content."
        except json.JSONDecodeError:
            return "Error: Could not decode response."
    
    return f"Error: {response.status_code} - {response.text}"

# Function to extract YouTube transcript
def get_youtube_transcript(video_url):
    if "youtu.be" in video_url:
        video_id = video_url.split("/")[-1]
    elif "youtube.com" in video_url:
        video_id = video_url.split("v=")[-1].split("&")[0]
    else:
        return "Invalid YouTube URL format"
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-GB', 'en-US'])
        return " ".join([t['text'] for t in transcript])
    except Exception as e:
        return f"Error: {str(e)}"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    images = []
    
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    for page in pdf_document:
        text += page.get_text("text") + "\n"
        images += page.get_images(full=True)

    if not text.strip():
        for img_index, img_info in enumerate(images):
            xref = img_info[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            text += pytesseract.image_to_string(image) + "\n"

    return text.strip()

# Tabs for YouTube and PDF
tab1, tab2 = st.tabs(["🎥 Summarize YouTube Video", "📄 Summarize PDF"])

# YouTube Summarization and Chatbot
with tab1:
    st.subheader("🎥 Summarize YouTube Video")
    video_url = st.text_input("Enter YouTube Video URL:")
    transcript_text = ""

    if video_url:
        with st.spinner("Fetching transcript..."):
            transcript_text = get_youtube_transcript(video_url)

        if transcript_text:
            st.success("Transcript fetched successfully!")
            with st.expander("📜 View Transcript"):
                st.write(transcript_text)

    # Chat interface
    if transcript_text:
        user_input = st.chat_input("Ask something about the video...")

        if user_input:
            if user_input.lower() in ["summarize", "summary", "give me a summary"]:
                with st.spinner("Generating summary..."):
                    summary = fetch_summary(transcript_text)
                st.subheader("📌 Summary:")
                st.write(summary)
            else:
                answer = fetch_answer(user_input, transcript_text)
                st.write(f"💬 **Answer:** {answer}")

# PDF Summarization and Chatbot
with tab2:
    st.subheader("📄 Summarize PDF")
    uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])
    pdf_text = ""

    if uploaded_file:
        with st.spinner("Extracting text..."):
            pdf_text = extract_text_from_pdf(uploaded_file)

        if pdf_text:
            st.success("Text extracted successfully!")
            with st.expander("📜 View Extracted Text"):
                st.write(pdf_text)

    # Chat interface
    if pdf_text:
        user_input = st.chat_input("Ask something about the PDF content...")

        if user_input:
            if user_input.lower() in ["summarize", "summary", "give me a summary"]:
                with st.spinner("Generating summary..."):
                    summary = fetch_summary(pdf_text)
                st.subheader("📌 Summary:")
                st.write(summary)
            else:
                answer = fetch_answer(user_input, pdf_text)
                st.write(f"💬 **Answer:** {answer}")

# Footer
st.markdown("---")
st.markdown("🔗 **Built with AI | Streamlit | Hugging Face**")
