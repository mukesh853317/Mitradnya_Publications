import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import textwrap
from fpdf import FPDF

# 1. PDF Generator (Fixed)
def create_pdf(text_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=8)
    for line in text_data.split('\n'):
        wrapped = textwrap.wrap(line, width=90)
        for w in wrapped:
            pdf.cell(0, 5, txt=w, ln=1)
    return bytes(pdf.output(dest='S'))

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>🏛️ 3.1 PRO - Board Paper Generator</h2>", unsafe_allow_html=True)
    
    # Load Data
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("Data file not found!")
        return
    qna_df = pd.read_csv(qna_path).astype(str).apply(lambda x: x.str.strip())
    
    # Tabs
    tab1, tab2 = st.tabs(["🏛️ Strict Board Paper", "📝 Custom Practice"])
    
    with tab2:
        st.markdown("### 📝 Custom Paper Generator")
        # Unique Keys (c_sub_unique)
        sub_list = qna_df['Subject'].unique()
        c_sub = st.selectbox("Select Subject:", sub_list, key="custom_sub_unique")
        
        c_chaps = st.multiselect("Select Chapters:", qna_df[qna_df['Subject'] == c_sub]['Chapter_Name'].unique(), key="custom_chaps_unique")
        
        # Checkboxes
        col1, col2, col3 = st.columns(3)
        with col1: use_prac = st.checkbox("Practical", True, key="chk_prac")
        with col2: use_short = st.checkbox("Short Notes", True, key="chk_short")
        with col3: use_theory = st.checkbox("Theory", True, key="chk_theory")
        
        if st.button("🚀 Generate Custom Paper", key="btn_gen_custom"):
            cats = []
            if use_prac: cats.append('Exercise_Problems')
            if use_short: cats.append('Short_Notes')
            if use_theory: cats.append('One_Sentence')
            
            paper = qna_df[(qna_df['Subject'] == c_sub) & (qna_df['Chapter_Name'].isin(c_chaps)) & (qna_df['Category'].isin(cats))]
            
            if not paper.empty:
                paper_txt = "MITRADNYA PUBLICATIONS - PAPER\n============================\n\n"
                
                for i, row in paper.iterrows():
                    st.markdown(f"**Q{i+1}:** {row['Question_Text']}")
                    paper_txt += f"Q{i+1}: {row['Question_Text']}\n\n"
                    
                    # AI Solution Expander
                    with st.expander(f"🤖 AI Solution for Q{i+1}"):
                        if st.button(f"Generate AI Answer {i+1}", key=f"ai_btn_{i}"):
                            with st.spinner("AI thinking..."):
                                try:
                                    model = genai.GenerativeModel('gemini-1.5-flash')
                                    res = model.generate_content(f"Solve: {row['Question_Text']}")
                                    st.info(res.text)
                                except: st.error("AI Error.")
                
                st.download_button("📥 Download PDF", data=create_pdf(paper_txt), file_name="Custom_Paper.pdf", mime="application/pdf")
            else:
                st.warning("No questions match your criteria!")

show_admin_panel()
