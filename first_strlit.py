import streamlit as st
import pandas as pd
from login import Login
import os
import pickle

# Initialize Login object
login_obj = Login()

# Streamlit App
st.title("Login and Contract Viewer")

# Option to input token directly

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
    else:
        st.error("Please enter all credentials before logging in.")

st.title("OR Login with token")

token_input = st.text_input("Token", placeholder="Enter your token directly", type="password")
# Logic to set the token
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
