import streamlit as st
import pandas as pd
from login import Login

# Initialize Login object
login_obj = Login()

# Initialize session state for trading symbols
if "tradingsymbols" not in st.session_state:
    st.session_state["tradingsymbols"] = pd.DataFrame(columns=["Trading Symbol"])

# Streamlit App
st.title("Login and Contract Viewer")

# Input boxes for user ID, password, and tpin
user_id = st.text_input("User ID", placeholder="Enter your user ID")
password = st.text_input("Password", placeholder="Enter your Password", type="password")
tpin = st.text_input("Tpin", placeholder="Enter your Tpin")

# Login logic
if st.button("Login"):
    if user_id and password and tpin:
        token = login_obj.login(user_id, password, tpin)
        st.session_state["token"] = token
        st.success("Login successful!")
        st.markdown("### Your Token")
        st.text(st.session_state["token"])
    else:
        st.error("Please enter all credentials before logging in.")

st.title("OR Login with Token")
token_input = st.text_input("Token", placeholder="Enter your token directly", type="password")
if st.button("Set Token"):
    if token_input:
        st.session_state["token"] = token_input
        st.success("Token has been set successfully!")
    else:
        st.error("Please enter a token.")

# Contract button
if st.button("Contract"):
    if st.session_state.get("token"):
        login_obj.generateContractFile(st.session_state["token"])
        df = pd.read_csv("zerodha_contractfile.csv")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("Please set a token or log in to view contract data.")

# CRUD for Trading Symbols
st.title("Manage Trading Symbols")

# Input for adding a trading symbol
new_symbol = st.text_input("Add Trading Symbol", placeholder="Enter a trading symbol")
if st.button("Add Symbol"):
    if new_symbol:
        # Check for duplicates
        if new_symbol in st.session_state["tradingsymbols"]["Trading Symbol"].values:
            st.warning(f"Trading symbol '{new_symbol}' already exists.")
        else:
            # Add the new symbol to the DataFrame
            st.session_state["tradingsymbols"] = pd.concat(
                [st.session_state["tradingsymbols"], pd.DataFrame({"Trading Symbol": [new_symbol]})],
                ignore_index=True
            )
            st.success(f"Trading symbol '{new_symbol}' added!")
    else:
        st.error("Please enter a trading symbol.")

# Display the table of trading symbols with a delete button
st.subheader("Current Trading Symbols")
if not st.session_state["tradingsymbols"].empty:
    for index, row in st.session_state["tradingsymbols"].iterrows():
        col1, col2 = st.columns([3, 1])  # Create columns for symbol and delete button
        with col1:
            st.write(row["Trading Symbol"])  # Display the trading symbol
        with col2:
            if st.button("Delete", key=f"delete_{index}"):
                st.session_state["tradingsymbols"] = st.session_state["tradingsymbols"].drop(index).reset_index(drop=True)
                st.experimental_set_query_params()  # Rerun to refresh the table
else:
    st.info("No trading symbols added yet.")
