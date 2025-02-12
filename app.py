import streamlit as st
import base64
import pytesseract
from PIL import Image
from firebase_config import db
from auth import login_user_func, signup_user_func
# from expense_manager import save_expense
from ocr_processor import extract_text_from_image
# from ai_classifier import classify_expense

st.set_page_config(layout="wide")



# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# Function to change pages
def switch_page(page):
    st.session_state["page"] = page


st.markdown("""
    <style>
    #main-title {
        color: rgb(0,234,0);
        font-size: 50px;
        
        font-weight: bold;
    }
    </style>
    
    <p id="main-title">ExpenSee!</p>
""", unsafe_allow_html=True)
st.divider()

#Login Home Page Content
if st.session_state["page"] == "Home":
   

    st.markdown("""
        <style>
    
        }
        .form-input {
            width: 50px !important;
            text-align: center;
        }
    
        .custom-btn {
            background-color: #007bff;
            color: white;
            padding: 8px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: 0.3s;
            font-size: 16px;
        }
        .custom-btn:hover {
            background-color: #0056b3;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create Login & Signup Toggle Buttons
    st.markdown('<div class="btn-container">', unsafe_allow_html=True)
 
    # Create columns to center the form in wide layout
    col1, col2, col3 = st.columns([2, 1, 3])  # Middle column will be wider
    with col1:
        st.markdown("""
        <style>
        #home_txt {
            font-size: 20px;
            color: rgb(255,255,255);
            padding-up:100px;
            style:italic;
        }
        </style>
        <br><br><br><br>
        <p id="home_txt">
            Expensee is your all-in-one expense management solution. Track your income and expenses, 
            create budgets, generate reports, and gain a clear understanding of your financial health. 
            Whether you're a student, a professional, or managing a household, Expensee makes 
            financial management easy and effective.
        </p>
    """, unsafe_allow_html=True)

    with col3: 

        st.markdown('<div class="form-container">', unsafe_allow_html=True)

        st.title("🔐 Login / Signup")

        option = st.radio("Select Option", ["Login", "Signup"], horizontal=True)

        if option == "Login":
            login_user = st.text_input("Username:")
            login_pass = st.text_input("Password:", type="password")
            if st.button("Login Now"):
                login_user_func(login_user,login_pass)
                

        elif option == "Signup":
            signup_name = st.text_input("Name:")
            signup_user = st.text_input("New Username:")
            signup_pass = st.text_input("New Password:", type="password")
            confirm_pass = st.text_input("Confirm Password:", type="password")
            if st.button("Create Account"):
                signup_user_func(signup_user,signup_pass,signup_name)
                
        st.markdown('</div>', unsafe_allow_html=True)


if st.session_state["page"] == "input":
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("INPUT", key="input_key", use_container_width=True):
            switch_page("input")

    with col2:
        if st.button("ANALYTICS", key="analytics_key", use_container_width=True):
            switch_page("analytics")

    with col3:
        if st.button("SUMMARY", key="summary_key", use_container_width=True):
            switch_page("summary")

    st.markdown("<br>", unsafe_allow_html=True)  # Space after navbar


    st.title("💰 Expense Tracker")

    # User selects how they want to input expenses
    option = st.radio("Choose Input Method:", ["Manual Entry", "Upload Bill"])

    if option == "Manual Entry":
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            amount = st.text_input("Enter Amount Spent:")
            category = st.selectbox("Select Category:", ["Food", "Games", "Shopping", "Other"])
            
            if st.button("Save Expense"):
                # db.collection("expenses").add({"amount": amount, "category": category})
                st.success("✅ Expense Saved!")

    elif option == "Upload Bill":
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            uploaded_file = st.file_uploader("Upload your Bill", type=["png", "jpg", "jpeg"])
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            extracted_text = extract_text_from_image(img)  # OCR Process
            
            st.write("📜 Extracted Text from Bill:")
            st.write(extracted_text)

            # **AI Classifier with Vertex AI will go here (Next Step)**
            st.write("🔍 AI is analyzing the text to detect category...")

            if st.button("Save AI-Classified Expense"):
                # Assume AI classified it as "Food"
                ai_classified_category = "Food"  
                # db.collection("expenses").add({"amount": "Auto-detected", "category": ai_classified_category})
                st.success(f"✅ Expense Saved under '{ai_classified_category}'!")