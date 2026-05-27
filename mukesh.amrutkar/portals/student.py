import streamlit as st
df = pd.read_csv(csv_path).dropna(subset=['Subject'])

def show_student_dashboard():
    st.title("🎓 Student Portal")
    st.write("Welcome! This is a simple student portal.")
    # डेटा लोड करण्याचे लॉजिक आपण नंतर हळूहळू ॲड करू शकतो
    st.info("Portal is working successfully!")
