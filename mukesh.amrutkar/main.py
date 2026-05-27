import streamlit as st
from portals import student
from portals import admin
from portals import parent
from utils import auth

def main():
    # १. लॉगिन स्टेट हाताळा
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # २. लॉगिन नसेल तर लॉगिन स्क्रीन
    if not st.session_state.logged_in:
        auth.show_login()
        return # लॉगिन नसेल तर पुढे काहीही रन करू नका

    # ३. लॉगिन असेल तरच पोर्टल लोड करा
    st.sidebar.success(f"Welcome, {st.session_state.get('username', 'User')}!")
    role = st.session_state.get("role", "Student") # डिफॉल्ट रोल 'Student' ठेवा

    # ४. सुरक्षित पोर्टल लोडिंग (Try-Except सह)
    try:
        if role == "Admin":
            admin.show_admin_panel()
        elif role == "Student":
            student.show_student_dashboard()
        elif role == "Parent":
            parent.show_parent_dashboard()
        else:
            st.error(f"अपरिचित रोल: {role}")
    except Exception as e:
        st.error(f"पोर्टल लोड करताना एरर आला: {e}")
        st.info("डेटा फाईलमध्ये 'Subject' कॉलम तपासा.")

    # ५. लॉगआउट बटण
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

if __name__ == "__main__":
    main()
