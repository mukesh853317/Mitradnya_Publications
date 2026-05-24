import streamlit as st

def show_login():
    st.subheader("🔐 Mitradnya's Portal - Login")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # हे फक्त टेस्टिंगसाठी आहे, नंतर आपण डेटाबेस वापरू
        if user == "mukesh" and password == "123":
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.role = "Admin" # हा रोल आपण नंतर बदलू शकतो
            st.rerun()
        else:
            st.error("Invalid Username or Password!")
