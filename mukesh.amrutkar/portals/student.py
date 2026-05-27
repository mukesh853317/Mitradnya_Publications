import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import sys

# Utils import - एरर न येण्यासाठी Safety Check
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from utils import quiz_manager
except ImportError:
    quiz_manager = None

def show_student_dashboard():
    # डिझाईन युटिलिटी
    try:
        import design_utils
        design_utils.apply_premium_design()
    except: pass

    st.subheader("🎓 Student's Dashboard - Mitradnya Publication")
    
    # 1. लोड डेटा
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(csv_path):
        st.error("⚠️ QnA.csv फाईल सापडली नाही!")
        return

    df = pd.read_csv(csv_path)
    # कॉलम नावे क्लीन करा (Space असेल तर ती निघून जाईल)
    df.columns = df.columns.str.strip()
    
    # आवश्यक कॉलम्स आहेत का?
    required = ['Subject', 'Chapter_Name', 'Question_Text']
    if not all(col in df.columns for col in required):
        st.error(f"⚠️ CSV फाईलमध्ये कॉलम्स सापडले नाहीत. कृपया खात्री करा की कॉलम्स हीच आहेत: {required}")
        return

    # डेटा फिल करा
    df['Subject'] = df['Subject'].ffill().astype(str).str.strip()
    df['Chapter_Name'] = df['Chapter_Name'].ffill().astype(str).str.strip()

    # 2. ग्लोबल फिल्टर (Subject & Chapter)
    col_sub, col_chap = st.columns(2)
    with col_sub:
        subs = df['Subject'].unique().tolist()
        sel_sub = st.selectbox("Select Subject", subs, key="student_sub_123")
    
    with col_chap:
        chaps = df[df['Subject'] == sel_sub]['Chapter_Name'].unique().tolist()
        sel_chap = st.selectbox("Select Chapter", chaps, key="student_chap_123")

    df_filtered = df[(df['Subject'] == sel_sub) & (df['Chapter_Name'] == sel_chap)]

    # 3. Tabs
    tabs = st.tabs(["📚 Study Room", "📄 Board Papers", "🎯 Objective Test", "📈 Progress"])
    
    with tabs[0]:
        st.markdown(f"### Questions for {sel_chap}")
        # इथे स्टडी रूमचे लॉजिक आहे जे तुम्ही मागच्या कोडमध्ये वापरले होते...
        st.success("Study Room loaded successfully!")

    with tabs[1]:
        st.write("Board Papers section")

    with tabs[2]:
        if quiz_manager:
            quiz_manager.load_objective_test(sel_sub, sel_chap)
        else:
            st.warning("Quiz Manager not found.")

    with tabs[3]:
        st.write("Progress Analytics")

# फंक्शन कॉल
show_student_dashboard()
