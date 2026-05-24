import streamlit as st

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard 🎓")
    st.write(f"Hello!!! {st.session_state.username}, Please Select One of the options below to Start Studying.")
    
    # टॅब्स वापरून विद्यार्थी पोर्टल
    tab1, tab2, tab3 = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
    
    with tab1:
        st.write("Your Short Notes will appear here.")
    with tab2:
        st.write("There will be Exercise Practice Problems here.")
    with tab3:
        st.write("There will be Extra Practical Questions here.")
