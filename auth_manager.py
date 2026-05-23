import streamlit as st

def check_login():
    """अट्रॅक्टिव्ह लॉगिन मॅनेजर"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        # लॉगिनसाठी एक छान कंटेनर (CSS मुळे हे सेंटरला दिसेल)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <style>
                .login-box {
                    padding: 2rem;
                    border-radius: 25px;
                    border: 1px solid #e6e6e6;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                </style>
                <div class="login-box">
                    <h2 style='text-align: center; color: #4F46E5;'>🎓 Mitradnya Publication's Portal 🎓</h2>
                    <p style='text-align: center;'>WELCOM<br>TO</br><br>📚 MITRADNYA PUBLICATIONS 📚</br>.</p></br>
                </div>
            """, unsafe_allow_html=True)
            
            user = st.text_input("👤 Username", placeholder="Enter your ID")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
            
            if st.button("🚀 Login Securely", use_container_width=True):
                if user == "admin" and password == "mukesh123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Credentials!")
        return False
    return True
