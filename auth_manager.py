import streamlit as st

def check_login():
    """Function to Manage Logins only"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.subheader("🔒 Login to Mitradnya's Portal")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == "admin" and password == "mukesh123": # इथे तुम्ही तुमचा पासवर्ड बदलू शकता
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials!")
        return False
    return True
