import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

# Initialize Firebase Admin SDK (Only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("edugenie-2025-firebase-adminsdk-fbsvc-7787f16a89.json")
    firebase_admin.initialize_app(cred)

# Firestore Database Client
db = firestore.client()

# Firebase Web Config (Replace with your Firebase Config)
firebaseConfig = {
    "apiKey": "AIzaSyC7eSehrx8PSD-FvCM5yZZOIkJXXnlTwVo",
    "authDomain": "edugenie-2025.firebaseapp.com",
    "projectId": "edugenie-2025",
    "storageBucket": "edugenie-2025.appspot.com",
    "messagingSenderId": "946937598029",
    "appId": "1:946937598029:web:035f99f2eb82b97d2e4c04",
    "databaseURL": "https://edugenie-2025-default-rtdb.firebaseio.com/"
}

# Initialize Pyrebase for Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth_pyrebase = firebase.auth()
