import streamlit as st
from utils import auth

# लॉगिन स्टेट तपासणे
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def main():
    if not st.session_state.logged_in:
        auth.show_login() # ही फाईल आता नीट काम करेल
    else:
        st.title(f"Welcome, {st.session_state.username}!")
        st.write("📚 Welcome to MITRADNYA PUBLICATION'S Portal 📚")
        
        # लॉगआउट बटण
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
