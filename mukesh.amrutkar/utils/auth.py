import streamlit as st
import pandas as pd
import os

def show_login():
    st.subheader("🔐 Login")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # फाईलचा पाथ
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'students.csv')
    
    if st.button("Login"):
        # फाईल आहे का ते चेक करणे
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            
            # लॉगिन लॉजिक (हे 'if' च्या आत असायला हवे)
            user_row = df[(df['Username'] == user) & (df['Password'].astype(str) == str(password))]
            
            if not user_row.empty:
                st.session_state.logged_in = True
                st.session_state.username = user
                st.session_state.role = user_row.iloc[0]['Role']
                st.rerun()
            else:
                st.error("Invalid Username or Password!")
        else:
            st.error(f"Error: Database file not found at {csv_path}")
