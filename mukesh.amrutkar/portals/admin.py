import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import datetime
import textwrap
from fpdf import FPDF

# PDF Generator Function (Optimized for 80 Marks Board Pattern)
def create_pdf(text_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=9)
    pdf.set_auto_page_break(auto=True, margin=15)
    clean_text = text_data.encode('latin-1', 'replace').decode('latin-1')
    for line in clean_text.split('\n'):
        wrapped_lines = textwrap.wrap(line, width=80, break_long_words=True, replace_whitespace=False)
        for w_line in wrapped_lines:
            pdf.multi_cell(0, 5, txt=w_line)
    out = pdf.output()
    return out.encode('latin-1') if isinstance(out, str) else bytes(out)

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>🏛️ 3.1 PRO - Board Paper Generator</h2>", unsafe_allow_html=True)
    
    # AI Config
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    except: pass
    
    # Load Data
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    qna_df = pd.read_csv(qna_path).astype(str).apply(lambda x: x.str.strip())
    all_subjects = qna_df['Subject'].unique().tolist()
    
    # Tabs: Strict Board Paper vs Custom
    tab1, tab2 = st.tabs(["🏛️ Strict Board Pattern", "📝 Custom Practice"])
    
    # Custom Practice Tab logic with Checkboxes
    with tab2:
        c_sub = st.selectbox("Select Subject:", all_subjects, key="c_sub")
        c_chaps = st.multiselect("Select Chapters:", sorted(qna_df[qna_df['Subject'] == c_sub]['Chapter_Name'].unique().tolist()), key="c_chaps")
        
        st.markdown("##### Select Question Types:")
        c1, c2, c3 = st.columns(3)
        with c1: use_prac = st.checkbox("Practical Problems", value=True)
        with c2: use_short = st.checkbox("Short Notes", value=True)
        with c3: use_theory = st.checkbox("Theory Questions", value=True)
        
        if st.button("🚀 Generate Custom Paper"):
            cats = []
            if use_prac: cats.append('Exercise_Problems')
            if use_short: cats.append('Short_Notes')
            if use_theory: cats.append('One_Sentence')
            
            paper = qna_df[(qna_df['Subject'] == c_sub) & (qna_df['Chapter_Name'].isin(c_chaps)) & (qna_df['Category'].isin(cats))]
            
            if paper.empty:
                st.warning("No questions found!")
            else:
                st.success(f"Generated {len(paper)} questions.")
                
                # Professional Preview
                paper_txt = "PROFESSIONAL PAPER\n\n"
                ans_txt = "AI GENERATED ANSWERS\n\n"
                
                for i, row in paper.iterrows():
                    st.write(f"**Q{i+1}:** {row['Question_Text']}")
                    paper_txt += f"Q{i+1}: {row['Question_Text']}\n\n"
                    
                    if st.button(f"🤖 Get AI Solution for Q{i+1}", key=f"ai_{i}"):
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content(f"Solve: {row['Question_Text']}")
                        st.info(f"Ans: {res.text}")
                        ans_txt += f"Ans {i+1}: {res.text}\n\n"
                
                col_d1, col_d2 = st.columns(2)
                with col_d1: st.download_button("📥 PDF Paper", data=create_pdf(paper_txt), file_name="Paper.pdf", mime="application/pdf")
                with col_d2: st.download_button("📥 PDF Answers", data=create_pdf(ans_txt), file_name="Answers.pdf", mime="application/pdf")

# Run
show_admin_panel()
