import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import textwrap
from fpdf import FPDF

# PDF Generator (Error-Free)
def create_safe_pdf(text_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=8)
    for line in text_data.split('\n'):
        wrapped = textwrap.wrap(line, width=90)
        for w in wrapped:
            pdf.cell(0, 5, txt=w, ln=1)
    return bytes(pdf.output(dest='S'))

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>Professional Paper Generator</h2>", unsafe_allow_html=True)
    
    # Load Data
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("Data file missing!")
        return
    df = pd.read_csv(qna_path).astype(str)
    
    # UI Layout
    sub = st.selectbox("Select Subject:", df['Subject'].unique(), key="pro_sub")
    chaps = st.multiselect("Select Chapters:", df[df['Subject'] == sub]['Chapter_Name'].unique(), key="pro_chaps")
    
    # Question Filters
    st.markdown("##### Question Type:")
    c1, c2, c3 = st.columns(3)
    with c1: prac = st.checkbox("Practical", True, key="pro_prac")
    with c2: short = st.checkbox("Short Notes", True, key="pro_short")
    with c3: theory = st.checkbox("Theory", True, key="pro_theory")
    
    if st.button("🚀 Generate Professional Paper"):
        cats = ['Exercise_Problems'] if prac else []
        if short: cats.append('Short_Notes')
        if theory: cats.append('One_Sentence')
        
        paper = df[(df['Subject'] == sub) & (df['Chapter_Name'].isin(chaps)) & (df['Category'].isin(cats))]
        
        if not paper.empty:
            paper_txt = "MITRADNYA PUBLICATION'S - BOARD PATTERN PAPER\n" + "="*60 + "\n\n"
            
            for i, row in paper.iterrows():
                st.markdown(f"**Q{i+1}:** {row['Question_Text']}")
                paper_txt += f"Q{i+1}: {row['Question_Text']}\n\n"
                
                # AI Tab per question
                with st.expander(f"Generate Solution {i+1}"):
                    if st.button(f"Click for Answer {i+1}", key=f"ai_{i}"):
                        with st.spinner("Generating..."):
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            res = model.generate_content(f"Solve: {row['Question_Text']}")
                            st.info(res.text)
                            paper_txt += f"Solution {i+1}: {res.text}\n\n"
            
            # PDF Download
            st.download_button("📥 Download Final PDF", data=create_safe_pdf(paper_txt), file_name="Professional_Paper.pdf", mime="application/pdf")
        else:
            st.warning("No questions found!")

show_admin_panel()
