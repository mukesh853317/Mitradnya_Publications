import streamlit as st
import pandas as pd
import os
import textwrap
from fpdf import FPDF

# Professional PDF Generator
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 15)
        self.cell(0, 10, "MITRADNYA PUBLICATIONS", 0, 1, 'C')
        self.set_font("Arial", '', 10)
        self.cell(0, 5, "Professional Board Pattern Examination", 0, 1, 'C')
        self.ln(10)

def create_professional_pdf(html_content):
    # आता आपण HTML वरून PDF बनवण्यासाठी simple text रूपांतरण वापरू जे क्रॅश होत नाही
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # रिप्लेसमेंट करून काही टॅग्स काढूया
    clean_text = html_content.replace("<br>", "\n").replace("<b>", "").replace("</b>", "").replace("<td>", " | ").replace("<tr>", "\n")
    
    for line in clean_text.split('\n'):
        if line.strip():
            pdf.multi_cell(0, 7, txt=line)
    return bytes(pdf.output(dest='S'))

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>🏛️ Mitradnya Professional Paper Generator</h2>", unsafe_allow_html=True)
    
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("⚠️ Data file not found!")
        return
    qna_df = pd.read_csv(qna_path).astype(str).apply(lambda x: x.str.strip())
    
    all_subjects = qna_df['Subject'].unique().tolist()
    sub = st.selectbox("Select Subject:", all_subjects)
    chaps = st.multiselect("Select Chapters:", sorted(qna_df[qna_df['Subject'] == sub]['Chapter_Name'].unique().tolist()))
    
    st.markdown("##### Select Question Types:")
    c1, c2, c3 = st.columns(3)
    with c1: prac = st.checkbox("Practical", value=True)
    with c2: short = st.checkbox("Short Notes", value=True)
    with c3: theory = st.checkbox("Theory", value=True)
    
    if st.button("🚀 Generate Professional Paper"):
        cats = []
        if prac: cats.append('Exercise_Problems')
        if short: cats.append('Short_Notes')
        if theory: cats.append('One_Sentence')
        
        paper = qna_df[(qna_df['Subject'] == sub) & (qna_df['Chapter_Name'].isin(chaps)) & (qna_df['Category'].isin(cats))]
        
        if not paper.empty:
            # Displaying in Professional HTML Format
            html_paper = f"<h3>Subject: {sub}</h3><hr>"
            for i, row in paper.iterrows():
                html_paper += f"<p><b>Q{i+1}.</b> {row['Question_Text']}</p>"
            
            st.markdown(html_paper, unsafe_allow_html=True)
            
            # Download
            st.download_button("📥 Download Professional PDF", data=create_professional_pdf(html_paper), file_name="Exam_Paper.pdf", mime="application/pdf")
        else:
            st.warning("No questions found!")

show_admin_panel()
