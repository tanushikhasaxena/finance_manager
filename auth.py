from firebase_config import db
import streamlit as st

def signup_user_func(username, password,name):
    """Creates a new user in Firebase"""
    user_ref = db.collection("users").document(username)
    user_ref.set({"name":name,"username": username, "password": password})
    st.success("✅ Account Created Successfully!")
    

def login_user_func(username, password):
    """Verifies user credentials"""
    user_ref = db.collection("users").document(username).get()
    if user_ref.exists:
        stored_password = user_ref.to_dict()["password"]
        if stored_password == password:
            st.success("✅ Login Successful!")
            st.session_state["page"] = "input"
            st.rerun()
            return True
        else:
            st.error("❌ Incorrect Password!")
            return False
    else:
        st.error("❌ User Not Found!")
        return False
