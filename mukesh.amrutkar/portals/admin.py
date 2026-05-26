import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import datetime
import textwrap
from fpdf import FPDF

# 1. FIXED PDF GENERATOR (Error-Free)
def create_pdf(text_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=8) # फॉन्ट साईज कमी केली जेणेकरून टेबल बसेल
    
    # मजकूर ९० विड्थमध्ये रॅप केला
    for line in text_data.split('\n'):
        wrapped_lines = textwrap.wrap(line, width=90, break_long_words=True)
        for w_line in wrapped_lines:
            pdf.cell(0, 5, txt=w_line, ln=1)
    
    return bytes(pdf.output(dest='S'))

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>🏛️ 3.1 PRO - Board Paper Generator</h2>", unsafe_allow_html=True)
    
    # AI Config
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    except: pass
    
    # Load Data
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("Data file missing!")
        return
    qna_df = pd.read_csv(qna_path).astype(str)
    
    # Tabs
    tab1, tab2 = st.tabs(["🏛️ Strict Board Paper", "📝 Custom Practice"])
    
    with tab2:
        st.markdown("### 📝 Custom Paper Generator")
        c_sub = st.selectbox("Select Subject:", qna_df['Subject'].unique(), key="c_sub")
        c_chaps = st.multiselect("Select Chapters:", qna_df[qna_df['Subject'] == c_sub]['Chapter_Name'].unique(), key="c_chaps")
        
        # Checkboxes for Question Types
        st.markdown("##### Select Question Types:")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1: prac = st.checkbox("Practical", True)
        with col_c2: short = st.checkbox("Short Notes", True)
        with col_c3: theory = st.checkbox("Theory", True)
        
        if st.button("🚀 Generate Custom Paper"):
            # Filter Logic
            cats = []
            if prac: cats.append('Exercise_Problems')
            if short: cats.append('Short_Notes')
            if theory: cats.append('One_Sentence')
            
            paper = qna_df[(qna_df['Subject'] == c_sub) & (qna_df['Chapter_Name'].isin(c_chaps)) & (qna_df['Category'].isin(cats))]
            
            if not paper.empty:
                paper_txt = "MITRADNYA PUBLICATIONS - PAPER\n============================\n\n"
                
                for i, row in paper.iterrows():
                    st.write(f"**Q{i+1}:** {row['Question_Text']}")
                    paper_txt += f"Q{i+1}: {row['Question_Text']}\n\n"
                    
                    # AI Solution Tab
                    with st.expander(f"🤖 Generate AI Solution for Q{i+1}"):
                        if st.button(f"Generate", key=f"ai_{i}"):
                            with st.spinner("AI solving..."):
                                model = genai.GenerativeModel('gemini-1.5-flash')
                                res = model.generate_content(f"Solve this: {row['Question_Text']}")
                                st.info(res.text)
                
                # Download Button
                st.download_button("📥 Download PDF Paper", data=create_pdf(paper_txt), file_name="Paper.pdf", mime="application/pdf")
            else:
                st.warning("No questions found!")

show_admin_panel()
