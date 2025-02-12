import firebase_admin
from firebase_admin import credentials, firestore

# Check if Firebase is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")  
    firebase_admin.initialize_app(cred)

# Firestore Database Connection
db = firestore.client()
