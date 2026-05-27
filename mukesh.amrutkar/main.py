import streamlit as st
from utils import auth
# main.py मधील सुधारित भाग
try:
    from portals import student, admin, parent
except Exception as e:
    st.error(f"पोर्टल लोड करताना एरर आला: {e}")

# आता ही खात्री करा की तुमची admin.py फाईल रिकामी आहे किंवा त्यात कोणताही सिंटॅक्स एरर नाही.

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def main():
    # लॉगिन स्टेट तपासा
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        # लॉगिन पेज (तुमचा जो आहे तोच ठेवा)
        pass 
    else:
        # रोलनुसार पोर्टल लोड करा
        role = st.session_state.get("role", "Student")
        
        # 🔴 येथे 'try-except' आणि 'import check' टाका
        if role == "Student":
            try:
                student.show_student_dashboard()
            except Exception as e:
                st.error(f"स्टुडंट पोर्टलमध्ये तांत्रिक अडचण: {e}")
                st.write("डेटा फाईलमध्ये 'Subject' कॉलमची स्पेलिंग तपासा.")
        elif role == "Admin":
            admin.show_admin_panel()
    else:
        st.sidebar.success(f"Welcome, {st.session_state.username}!")
        role = st.session_state.role
        
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
