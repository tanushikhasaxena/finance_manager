from firebase_config import db
import streamlit as st



def signup_user_func(username, password,name):
    """Creates a new user in Firebase"""
    user_ref = db.collection("users").document(username)
    user_doc = user_ref.get()

    personal_details = {"name":name,"username": username, "password": password}
    
    if user_doc.exists:
        st.error("User already exists!")
    else:
        user_ref.set({"personal details": [personal_details]})
        st.session_state["logged_in_user"] = username
        st.success("✅ Account Created Successfully!")
    

def login_user_func(username, password):
    """Login User from Firestore"""
    user_ref = db.collection("users").document(username).get()

    if not user_ref.exists:
        st.warning("⚠️ User not found! Please check your username.")
        return False

    user_data = user_ref.to_dict()

    # ✅ Check if 'personal_info' field exists
    if "personal details" not in user_data or "password" not in user_data["personal details"][0]:
        st.warning("⚠️ Password field missing in database!")
        return False

    stored_password = user_data["personal details"][0]["password"]

    if stored_password == password:
        st.success(f"✅ Welcome, {username}!")
        st.session_state["page"] = "input"

        st.session_state["logged_in_user"] = username  # ✅ Store session
        return True
    else:
        st.warning("❌ Incorrect password!")
        return False





def plot_monthly_expense(df):
    
    if df.empty:
        st.warning("⚠️ No data to plot!")
        return

    df["month"] = df["timestamp"].dt.strftime("%b %Y")  
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")  
    df = df.dropna(subset=["amount"])  
    df["amount"] = df["amount"].astype(int) 

    categories = ["Food", "Clothes", "Games", "Study", "Mandatory", "Others"]
    df = df[df["category"].isin(categories)]  

    # Group by month and category
    monthly_expense = df.groupby(["month", "category"])["amount"].sum().reset_index()

