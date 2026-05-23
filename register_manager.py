import streamlit as st

def show_registration():
    st.subheader("📝 Register New Student")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")
    
    if st.button("Register Now"):
        if new_pass == confirm_pass:
            # इथे तुम्ही ही माहिती एका फाईलमध्ये किंवा डेटाबेसमध्ये सेव्ह करू शकता
            st.success(f"User {new_user} registered successfully! Please login.")
        else:
            st.error("Passwords do not match!")
