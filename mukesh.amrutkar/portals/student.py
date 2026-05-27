import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import sys

# Utils import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from utils import quiz_manager
except ImportError:
    quiz_manager = None

def show_student_dashboard():
    st.subheader("🎓 Student's Dashboard - Mitradnya Publication")

    # API Configuration
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    except:
        st.error("API Key missing!")

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(csv_path):
        st.error("QnA.csv not found!")
        return

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    
    # ग्लोबल फिल्टर
    subject_list = df['Subject'].dropna().unique().tolist()
    selected_subject = st.selectbox("Select Subject", subject_list)
    
    chapter_list = df[df['Subject'] == selected_subject]['Chapter_Name'].dropna().unique().tolist()
    selected_chapter = st.selectbox("Select Chapter", chapter_list)
    
    df_filtered = df[(df['Subject'] == selected_subject) & (df['Chapter_Name'] == selected_chapter)]

    # Tabs
    main_tabs = st.tabs(["📚 Study Room", "📄 Board Papers", "🎯 Objective Test"])
    
    with main_tabs[0]:
        categories = ["IMP_Proforma", "Short_Notes", "One_Sentence", "Exercise_Problems", "Extra_Practical"]
        sub_tabs = st.tabs(categories)
        
        for i, cat_name in enumerate(categories):
            with sub_tabs[i]:
                cat_df = df_filtered[df_filtered['Category'] == cat_name]
                for idx, row in cat_df.iterrows():
                    q_text = str(row.get('Question_Text', ''))
                    with st.expander(f"{q_text[:50]}..."):
                        st.markdown(q_text)
                        if st.button("🧠 Generate Solution", key=f"btn_{cat_name}_{idx}"):
                            with st.spinner("⏳ AI is thinking..."):
                                model = genai.GenerativeModel('gemini-1.5-flash')
                                prompt = f"Expert Commerce Teacher: Solve this: {q_text}"
                                response = model.generate_content(prompt)
                                st.markdown(response.text)

    with main_tabs[1]:
        st.write("Board Papers section")

    with main_tabs[2]:
        if quiz_manager:
            quiz_manager.load_objective_test(selected_subject, selected_chapter)
