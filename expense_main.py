import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Smart Expense Tracker", page_icon="💰", layout="centered")

st.title("💰 AI Smart Expense Tracker & Budget Advisor")
st.write("Track your daily expenses, analyze spending patterns, and stay on top of your budget effortlessly!")

# Initialize session state for expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount ($)", "Description"])

with st.form("expense_form"):
    st.subheader("Add a New Expense")
    category = st.selectbox("Category", ["Food & Groceries", "Utilities", "Entertainment", "Transportation", "Other"])
    amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
    description = st.text_input("Description / Notes")
    submit_button = st.form_submit_button("Add Expense")

    if submit_button and amount > 0:
        new_data = pd.DataFrame({"Category": [category], "Amount ($)": [amount], "Description": [description]})
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_data], ignore_index=True)
        st.success("Expense added successfully!")

# Display Expense Log
if not st.session_state.expenses.empty:
    st.subheader("📊 Expense Summary")
    st.dataframe(st.session_state.expenses, use_container_width=True)

    total_spent = st.session_state.expenses["Amount ($)"].sum()
    st.metric(label="Total Spent", value=f"${total_spent:.2f}")

    # Spending by Category Chart
    st.subheader("📈 Spending Breakdown")
    category_summary = st.session_state.expenses.groupby("Category")["Amount ($)"].sum()
    fig, ax = plt.subplots()
    category_summary.plot(kind="bar", ax=ax, color="#ff4b4b")
    ax.set_ylabel("Amount ($)")
    st.pyplot(fig)
else:
    st.info("No expenses recorded yet. Add your first expense above!")
