import streamlit as st
from utils import auth
# तिन्ही पोर्टल्स इम्पोर्ट करा (जर फाईल्स नसतील तर बनवून ठेवा)
from portals import student, admin, parent 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def main():
    if not st.session_state.logged_in:
        auth.show_login()
    else:
        st.sidebar.success(f"Welcome, {st.session_state.username}!")
        role = st.session_state.role
        
        # आता हे तिन्ही फंक्शन्स ओळखले जातील
        if role == "Admin":
            admin.show_admin_panel()
        elif role == "Student":
            student.show_student_dashboard()
        elif role == "Parent":
            parent.show_parent_dashboard()
            
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
