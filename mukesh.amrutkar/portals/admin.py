import streamlit as st

def show_admin_panel():
    st.title("👨‍🏫 Admin Portal")
    st.write("Welcome Admin! Here you can manage questions.")
    # बेसिक फंक्शन
    if st.button("Check Database Status"):
        st.success("Database is ready to be loaded.")
