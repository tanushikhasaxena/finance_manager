import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
from firebase_admin import firestore

import streamlit as st
import pandas as pd
import plotly.express as px
db = firestore.client()

def fetch_expense_data(user_id):
    """Fetch user expenses from Firestore and convert to Pandas DataFrame"""
    user_ref = db.collection("users").document(user_id).get()

    if not user_ref.exists:
        print("⚠️ User not found!")
        return pd.DataFrame()  # Empty DataFrame

    user_data = user_ref.to_dict()
    
    if "expenses" not in user_data:
        print("⚠️ No expenses found for user!")
        return pd.DataFrame()  # Empty DataFrame

    # Convert expenses to DataFrame
    df = pd.DataFrame(user_data["expenses"])
    
    # Convert timestamp to datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d_%H-%M-%S")

    return df



import streamlit as st
import pandas as pd
import plotly.express as px

def plot_monthly_expense(df):
    """📊 Plot Monthly Expense Analysis in Streamlit"""
    if df.empty:
        st.warning("⚠️ No data to plot!")
        return

    # 🗓 Convert Timestamp to "Month Year"
    df["month"] = df["timestamp"].dt.strftime("%b %Y")  
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")  
    df = df.dropna(subset=["amount"])  
    df["amount"] = df["amount"].astype(int)

    categories = ["Food", "Clothes", "Games", "Study", "Mandatory", "Others"]
    df = df[df["category"].isin(categories)]  

    # ✅ Group by month and category
    monthly_expense = df.groupby(["month", "category"])["amount"].sum().reset_index()

    # 📊 Interactive Plotly Bar Chart
    fig = px.bar(
        monthly_expense, 
        x="month", 
        y="amount", 
        color="category", 
        barmode="group", 
        title="📊 Monthly Expense Analysis",
        labels={"amount": "Total Expense", "month": "Month"},
        hover_name="category",  # ✅ Hover par category highlight hogi
        hover_data={"month": True, "amount": True, "category": False},  # ✅ Month & Amount dikhega, Category auto highlight
        opacity=0.7  # 🔹 Non-hovered bars ko light karega
    )

    fig.update_layout(
        xaxis=dict(tickangle=0),  # 🔹 X-axis readable
        hovermode="closest",  # ✅ Hover ek hi point pe rahega
        plot_bgcolor="black",  # 🔹 Dark Theme
        paper_bgcolor="black",
        font=dict(color="white")  # 🔹 Text white rahega
    )

    st.plotly_chart(fig, use_container_width=True)  # ✅ Streamlit me show karo


def plot_daily_expense(df):
    """📈 Plot Daily Expense Analysis in Streamlit"""
    if df.empty:
        st.warning("⚠️ No data to plot!")
        return

    # 🗓 Convert Timestamp to "Day-Month Year"
    df["day"] = df["timestamp"].dt.strftime("%d %b %Y")  
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")  
    df = df.dropna(subset=["amount"])  
    df["amount"] = df["amount"].astype(int)

    categories = ["Food", "Clothes", "Games", "Study", "Mandatory", "Others"]
    df = df[df["category"].isin(categories)]  

    # ✅ Group by day and category
    daily_expense = df.groupby(["day", "category"])["amount"].sum().reset_index()

    # 📈 Interactive Line Graph
    fig = px.line(
        daily_expense, 
        x="day", 
        y="amount", 
        color="category", 
        markers=True,  # ✅ Points dikhne chahiye
        line_shape="spline",  # 🔹 Smooth lines
        hover_name="category",  # ✅ Hover pe category dikhegi
        title="📈 Daily Expense Trends"
    )

    fig.update_traces(
        mode="lines+markers", 
        marker=dict(size=8),  # 🔹 Bigger points
        hoverinfo="x+y+name"  # ✅ Only show relevant info
    )

    fig.update_layout(
        xaxis=dict(tickangle=0), 
        hovermode="closest",  # ✅ Saare points ek hi hover pe dikhaye
        plot_bgcolor="black", 
        paper_bgcolor="black",
        font=dict(color="white")  # 🔹 Dark Theme ke liye white text
    )

    st.plotly_chart(fig, use_container_width=True)  # ✅ Fix container issue
