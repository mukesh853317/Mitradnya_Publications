import streamlit as st
import pandas as pd
import os

def show_login():
    st.subheader("🔐 Login")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # CSV फाईल वाचणे
        df = pd.read_csv('data/students.csv')
        
        # चेक करणे: युजर आणि पासवर्ड जुळतो का?
        user_row = df[(df['Username'] == user) & (df['Password'].astype(str) == str(password))]
        
        if not user_row.empty:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.role = user_row.iloc[0]['Role']
            st.rerun()
        else:
            st.error("Invalid Username or Password!")
