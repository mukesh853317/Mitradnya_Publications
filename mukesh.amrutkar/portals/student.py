import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard 🎓")
    st.write(f"Hello!!! {st.session_state.username}, Please Select One of the options below to Start Studying.")

    # प्रश्नांची फाईल वाचणे
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    
    # टॅब्स वापरून विद्यार्थी पोर्टल
    tab1, tab2, tab3 = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
    
    with tab1:
        st.write("### Short Notes")
            # येथे फक्त 'Short_Notes' कॅटेगरीचे प्रश्न फिल्टर करा
            notes = df[df['Category'] == 'Short_Notes']
            st.table(notes[['Question_Text']])
        
    with tab2:
        st.write("### Exercise Problems")
            ex = df[df['Category'] == 'Exercise_Problems']
            st.table(ex[['Question_Text']])
        
    with tab3:
        st.write("### Extra Practical")
            prac = df[df['Category'] == 'Extra_Practical']
            st.table(prac[['Question_Text']])

else:
        st.error("Data File Not Found!")
