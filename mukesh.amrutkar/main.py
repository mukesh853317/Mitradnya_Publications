import streamlit as st
from portals import admin, student

def main():
    st.sidebar.title("Navigation")
    portal = st.sidebar.radio("Go to:", ["Student Portal", "Admin Portal"])
    
    if portal == "Student Portal":
        student.show_student_dashboard()
    else:
        admin.show_admin_panel()

if __name__ == "__main__":
    main()
