import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
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

# Function to show professional paper
def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>Board Paper Generator</h2>", unsafe_allow_html=True)
    
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    df = pd.read_csv(qna_path)

    # 1. Subject Selection
    sub = st.selectbox("Select Subject:", df['Subject'].unique())
    
    # 2. Section Based Paper Structure
    if st.button("🚀 Generate Professional Paper"):
        # Section A: Objective (Q.1)
        st.markdown("### Q.1 Objective Questions (20 Marks)")
        # इथे फक्त Objective डेटा फिल्टर करा
        
        # Section B: Practical (Q.2 onwards)
        st.markdown("### Q.2 Solve Practical Problems (10 Marks)")
        
        # इथे आपण i+1 ऐवजी फिक्स Q नंबर वापरू
        paper = df[df['Subject'] == sub].sample(5) 
        
        for idx, row in enumerate(paper.iterrows()):
            # इथे row['Question_Text'] प्रिंट करा
            st.markdown(f"**Q.{idx+2}:** {row[1]['Question_Text']}")
            
            # AI Button (Solution Tab)
            with st.expander(f"View Solution for Q.{idx+2}"):
                if st.button(f"Generate Solution", key=f"sol_{idx}"):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    res = model.generate_content(f"Solve this accounting problem professionally: {row[1]['Question_Text']}")
                    st.info(res.text)

show_admin_panel()
