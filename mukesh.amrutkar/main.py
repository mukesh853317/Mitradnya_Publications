import streamlit as st
from portals import student, admin, parent
from utils import auth

def main():
    # १. लॉगिन स्टेट तपासा
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # २. लॉगिन नाही तर लॉगिन पेज दाखवा
    if not st.session_state.logged_in:
        auth.show_login()
    else:
        # ३. लॉगिन असेल तर रोलनुसार पोर्टल लोड करा
        st.sidebar.success(f"Welcome, {st.session_state.get('username', 'User')}!")
        role = st.session_state.get("role", "Student")
        
        if role == "Admin":
            admin.show_admin_panel()
        elif role == "Student":
            try:
                student.show_student_dashboard()
            except Exception as e:
                st.error(f"स्टुडंट पोर्टल लोड करताना एरर: {e}")
        elif role == "Parent":
            parent.show_parent_dashboard()
            
        # ४. लॉगआउट बटण
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()

if __name__ == "__main__":
    main()
