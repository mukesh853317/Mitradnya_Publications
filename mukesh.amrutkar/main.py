import streamlit as st
from utils import auth

st.set_page_config(page_title="Mitradnya Publications", layout="wide")

def main():
    # लॉगिन नसेल तर लॉगिन दाखवा, असेल तर मेन डॅशबोर्ड दाखवा
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        auth.show_login()
    else:
        st.sidebar.success(f"Welcome {st.session_state.username}!")
        # इथे आपण 'Role' नुसार डॅशबोर्ड दाखवू
        if st.session_state.role == "Student":
            # import portals.student as student; student.show()
            st.write("Student Dashboard")
        elif st.session_state.role == "Parent":
            st.write("Parent Dashboard")

if __name__ == "__main__":
    main()
