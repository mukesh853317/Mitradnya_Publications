import streamlit as st
from portals import admin, student

def main():
    st.sidebar.title("Navigation")
    portal = st.sidebar.radio("Go to:", ["Student Portal", "Admin Portal", "Parent Portal"])
    
    if portal == "Student Portal":
        student.show_student_dashboard()
    elif role == "Parent Portal":
        parent.show_parent_dashboard()
    else:
        admin.show_admin_panel()
    
# लॉगआउट बटण शेवटी
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
if __name__ == "__main__":
    main()
