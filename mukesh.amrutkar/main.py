# main.py मध्ये लॉगिन झाल्यावर हा भाग वापरा:
if st.session_state.logged_in:
    role = st.session_state.role
    
    if role == "Admin":
        st.write("Welcome Admin! Manage your Publication here.")
    elif role == "Student":
        # इथे आपण portals/student.py ला कॉल करू
        st.write("Welcome Student! Start your learning.")
    elif role == "Parent":
        # इथे आपण portals/parent.py ला कॉल करू
        st.write("Welcome Parent! Monitor your child's progress.")
