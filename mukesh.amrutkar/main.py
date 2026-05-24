import streamlit as st
from utils import auth

# सर्वात आधी हे चेक करा (हे खूप महत्त्वाचे आहे)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def main():
    # आता 'if' कंडीशन वापरा, एरर येणार नाही
    if not st.session_state.logged_in:
        auth.show_login()
    else:
        st.sidebar.success(f"Welcome, {st.session_state.username}!")
        role = st.session_state.role
        
        if role == "Admin":
            st.write("Welcome Admin! Manage your Publication here.")
        elif role == "Student":
            from portals import student  # हे पोर्टल इम्पोर्ट करा
            student.show_student_dashboard()  # हे फंक्शन रन करा
            st.write("Welcome Student! Start your learning.")
        elif role == "Parent":
            st.write("Welcome Parent! Monitor your child's progress.")
            
        # लॉगआउट बटण
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
