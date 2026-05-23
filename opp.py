import streamlit as st
import pandas as pd
import smtplib
import requests
import urllib.parse
from email.mime.text import MIMEText
import random
import streamlit.components.v1 as components
import re
import os
import google.generativeai as genai

# --- Page Config ---
st.set_page_config(page_title="📚 Mitradnya Publication's Online Exam 📚", page_icon="📝", layout="centered")

# --- Authentication State ---
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'test_status' not in st.session_state:
    st.session_state.test_status = 'not_started'

# --- Data Loading ---
@st.cache_data
def load_all_data():
    try:
        # 1. Load Main CSV
        df = pd.read_csv('All in one.csv')
        df.columns = df.columns.str.strip()
        
        # 2. Load and Prepare QnA CSV
        qna_df = pd.read_csv('QnA.csv')
        qna_df.columns = qna_df.columns.str.strip()
        qna_df['Chapter_Name'] = qna_df['Chapter_Name'].ffill()
        qna_df['Category'] = qna_df['Category'].ffill()
        return df, qna_df
    except:
        return None, None

df, qna_df = load_all_data()

# --- Main App Interface ---
st.sidebar.markdown("## 📚 Mitradnya Publication's")
if df is not None:
    chapter_col = df.columns[0]
    selected_chapter = st.sidebar.selectbox("Select Chapter:", df[chapter_col].unique())
    
    st.title("📚 Mitradnya Publication's Portal")
    
    # 3 Tabs
    tab1, tab2, tab3 = st.tabs(["📝 Exam", "📖 Study Room", "📓 Q & A Bank"])
    
    with tab3:
        if qna_df is not None:
            cat_tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
            categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
            
            for i, cat_tab in enumerate(cat_tabs):
                with cat_tab:
                    filtered_df = qna_df[
                        (qna_df['Chapter_Name'].str.contains(str(selected_chapter), case=False, na=False)) & 
                        (qna_df['Category'] == categories[i])
                    ]
                    
                    if not filtered_df.empty:
                        for idx, row in filtered_df.iterrows():
                            with st.expander(f"Question: {row['Question_Text'][:40]}..."):
                                st.markdown("### 📝 Full Problem Statement:")
                                st.write(row['Question_Text'])
                                
                                if st.button("🧠 Generate Solution", key=f"btn_{idx}"):
                                    with st.spinner("⏳ AI is calculating..."):
                                        try:
                                            # API Key Setup
                                            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                                            model = genai.GenerativeModel('gemini-1.5-flash')
                                            response = model.generate_content(f"Solve this accountancy problem in Tally format: {row['Question_Text']}")
                                            st.markdown(response.text)
                                        except Exception as e:
                                            st.error(f"AI Error: {e}")
                    else:
                        st.info("या चॅप्टरमध्ये सध्या प्रश्न नाहीत.")
        else:
            st.error("QnA डेटा फाईल सापडली नाही.")

    # --- Exam Logic (Tab 1) ---
    with tab1:
        st.write("Exam Portal Content...")
else:
    st.error("डेटा फाईल्स (All in one.csv & QnA.csv) सापडत नाहीत. कृपया त्या GitHub वर अपलोड केल्याची खात्री करा.")
