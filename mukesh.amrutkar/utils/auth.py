import streamlit as st
import pandas as pd
import os

def show_login():
    def show_login():
    # फाईलचा पाथ नीट शोधण्यासाठी हा बदल करा
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'students.csv')
    
    # चेक करा की फाईल अस्तित्वात आहे का
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        st.error(f"Error: फाईल सापडली नाही! {csv_path}")
        return        
        # चेक करणे: युजर आणि पासवर्ड जुळतो का?
        user_row = df[(df['Username'] == user) & (df['Password'].astype(str) == str(password))]
        
        if not user_row.empty:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.role = user_row.iloc[0]['Role']
            st.rerun()
        else:
            st.error("Invalid Username or Password!")
