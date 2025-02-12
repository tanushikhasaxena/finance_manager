from firebase_config import db
import streamlit as st
import time
import uuid
from firebase_admin import firestore  # ✅ Firestore ko import kar

def save_expense(user_id, category, amount):
    """Save expense inside user's document"""
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    
    expense_data = {
        "category": category,
        "amount": amount,
        "timestamp": timestamp
    }
    
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_ref.update({"expenses": firestore.ArrayUnion([expense_data])})  # ✅ Add expense to list
    else:
        user_ref.set({"expenses": [expense_data]})  # ✅ Create user with first expense

    st.success(f"✅ Expense saved for user {user_id}")
