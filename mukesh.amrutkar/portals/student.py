import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("📚 Study Room - Mitradnya Publication's")
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_path, 'data', 'QnA.csv')    
    # फाईल लोड करणे
    try:
        df = pd.read_csv('mukesh.amrutkar/data/QnA.csv')
        df.columns = df.columns.str.strip() # स्पेस काढणे
        # फिल्टरिंग
        subject = st.selectbox("Select Subject", df['Subject'].unique())
        chapter = st.selectbox("Select Chapter", df[df['Subject'] == subject]['Chapter_Name'].unique())
        # टेबल दाखवणे
        filtered_df = df[(df['Subject'] == subject) & (df['Chapter_Name'] == chapter)]
        # डेटा नीट दिसण्यासाठी टेबल फॉरमॅट
        st.write(f"### {chapter} चे प्रश्न:")
        st.dataframe(
            filtered_df[['Category', 'Question_Text', 'Answer_or_Hint']], 
            use_container_width=True,
            hide_index=True
        )
        
    except Exception as e:
        st.error(f"डेटा लोड करताना अडचण आली: {e}")
    st.title("🎓 Student Portal")
    st.write("Welcome! This is a simple student portal.")
    # डेटा लोड करण्याचे लॉजिक आपण नंतर हळूहळू ॲड करू शकतो
    st.info("Portal is working successfully!")
