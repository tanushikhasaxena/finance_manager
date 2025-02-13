import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
from firebase_admin import firestore
from datetime import datetime
import datetime as dt

db = firestore.client()

def fetch_expense_data(user_id):
    """Fetch user expenses from Firestore and convert to Pandas DataFrame"""
    user_ref = db.collection("users").document(user_id).get()

    if not user_ref.exists:
        print("⚠️ User not found!")
        return pd.DataFrame() 
    user_data = user_ref.to_dict()
    
    if "expenses" not in user_data:
        print("⚠️ No expenses found for user!")
        return pd.DataFrame()  

    # Convert expenses to DataFrame
    df = pd.DataFrame(user_data["expenses"])
    
    # Convert timestamp to datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d_%H-%M-%S")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")  # ✅ Convert to datetime
    df["month"] = df["timestamp"].dt.strftime("%b %Y")  # ✅ Extract month

    return df


def plot_monthly_expense(df, selected_month=None):
    """📊 Plot Monthly Expense Analysis in Streamlit"""
    if df.empty:
        st.warning("⚠️ No data to plot!")
        return

    df["month"] = df["timestamp"].dt.strftime("%b %Y")  
    
    # Default: Current Month
    if selected_month is None:
        selected_month = dt.datetime.now().strftime("%b %Y")

    df = df[df["month"] == selected_month]

    categories = ["Food", "Clothes", "Games", "Study", "Mandatory", "Others"]
    df = df[df["category"].isin(categories)]  

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")  
    df = df.dropna(subset=["amount"])  
    df["amount"] = df["amount"].astype(int)

    monthly_expense = df.groupby(["month", "category"])["amount"].sum().reset_index()

    if monthly_expense.empty:
        st.warning(f"⚠️ No expenses recorded for {selected_month}!")
        return

    fig = px.bar(
        monthly_expense, 
        x="month", 
        y="amount", 
        color="category", 
        barmode="group", 
        title=f"📊 Monthly Expense Analysis - {selected_month}",
        labels={"amount": "Total Expense", "month": "Month"},
        hover_name="category",
        hover_data={"month": True, "amount": True, "category": False},  
        opacity=0.85  
    )

    fig.update_layout(
        xaxis=dict(tickangle=0),
        hovermode="closest",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
    )

    st.plotly_chart(fig, use_container_width=True, key=f"monthly_expense_chart_{selected_month}_{uuid.uuid4()}")  


def plot_daily_expense(df, selected_month=None):
    """📈 Plot Daily Expense Analysis in Streamlit for Selected Month"""
    if df.empty:
        st.warning("⚠️ No data to plot!")
        return

    df["month"] = df["timestamp"].dt.strftime("%b %Y")  
    df["day"] = df["timestamp"].dt.strftime("%d %b %Y") 
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")  
    df = df.dropna(subset=["amount"])  
    df["amount"] = df["amount"].astype(int)

    if selected_month is None:
        selected_month = dt.datetime.now().strftime("%b %Y")

    filtered_df = df[df["month"] == selected_month]

    if filtered_df.empty or filtered_df["amount"].sum() == 0:
        st.warning(f"⚠️ No expenses recorded for {selected_month}!")
        return  

    categories = ["Food", "Clothes", "Games", "Study", "Mandatory", "Others"]
    filtered_df = filtered_df[filtered_df["category"].isin(categories)]  

    daily_expense = filtered_df.groupby(["day", "category"])["amount"].sum().reset_index()

    fig = px.line(
        daily_expense, 
        x="day", 
        y="amount", 
        color="category", 
        markers=True,  
        line_shape="spline",  
        hover_name="category",  
        title=f"📈 Daily Expense Trends - {selected_month}"
    )

    fig.update_traces(
        mode="lines+markers", 
        marker=dict(size=8),  
        hoverinfo="x+y+name"  
    )

    fig.update_layout(
        xaxis=dict(tickangle=0), 
        hovermode="closest",  
        plot_bgcolor="black", 
        paper_bgcolor="black",
        font=dict(color="white")  
    )

    st.plotly_chart(fig, use_container_width=True, key=f"daily_expense_chart_{selected_month}_{uuid.uuid4()}")
