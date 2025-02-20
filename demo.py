import os
import requests
import json
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Correct API URL
api_url = "https://api.groq.com/openai/v1/chat/completions"

# Headers
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Function to check API status
def check_api():
    """Check if Groq API is reachable."""
    
    # ✅ Send a test request
    test_payload = {
        "model": "llama2-70b-chat",  # Ensure this model is supported
        "messages": [{"role": "user", "content": "Hello, can you respond?"}],
        "temperature": 0.7
    }

    response = requests.post(api_url, headers=headers, json=test_payload)

    if response.status_code == 200:
        print("✅ API is reachable and model is available!")
        print("Response:", response.json())  # Print response for debugging
    elif response.status_code == 503:
        print("⚠️ Model is loading, try again later.")
    elif response.status_code == 401:
        print("❌ Unauthorized: Check your API key in the .env file.")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

# Run API health check
check_api()
