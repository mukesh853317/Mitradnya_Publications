import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import textwrap
from fpdf import FPDF

# AI Configuration
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    pass

# PDF Generator Function
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
    st.markdown("<h2 style='color: #1e3a8a;'>👨‍🏫 Admin Portal - AI Paper Generator</h2>", unsafe_allow_html=True)
    
    # Load Data
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("⚠️ QnA.csv file missing!")
        return
    qna_df = pd.read_csv(qna_path).astype(str).apply(lambda x: x.str.strip())
    
    all_subjects = qna_df['Subject'].unique().tolist()
    selected_sub = st.selectbox("🎯 Select Subject:", all_subjects)
    
    all_chaps = sorted(qna_df[qna_df['Subject'] == selected_sub]['Chapter_Name'].unique().tolist())
    selected_chaps = st.multiselect("📑 Select Chapters:", all_chaps, default=all_chaps[:1])
        
    # Question Types
    st.markdown("##### 🎯 Select Question Types:")
    c1, c2, c3 = st.columns(3)
    with c1: use_prac = st.checkbox("Practical Problems", value=True)
    with c2: use_short = st.checkbox("Short Notes", value=True)
    with c3: use_theory = st.checkbox("Theory Questions", value=True)
    
    if st.button("🚀 Generate Paper & AI Solutions"):
        cats = []
        if use_prac: cats.append('Exercise_Problems')
        if use_short: cats.append('Short_Notes')
        if use_theory: cats.append('One_Sentence')
        
        paper = qna_df[(qna_df['Subject'] == selected_sub) & 
                       (qna_df['Chapter_Name'].isin(selected_chaps)) & 
                       (qna_df['Category'].isin(cats))]
        
        if paper.empty:
            st.warning("⚠️ No questions found for these selections!")
        else:
            st.success(f"✅ {len(paper)} questions generated.")
            
            paper_txt = "QUESTION PAPER\n\n"
            ans_txt = "AI GENERATED ANSWER KEY\n\n"
            
            # Display & AI
            for i, row in paper.iterrows():
                st.write(f"**Q{i+1}:** {row['Question_Text']}")
                paper_txt += f"Q{i+1}: {row['Question_Text']}\n\n"
                
                with st.expander(f"Generate Answer for Q{i+1}"):
                    if st.button(f"Generate Solution {i+1}", key=f"ai_{i}"):
                        with st.spinner("AI is thinking..."):
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            response = model.generate_content(f"Answer: {row['Question_Text']}")
                            st.info(f"**Ans:** {response.text}")
                            ans_txt += f"Ans {i+1}: {response.text}\n\n"
            
            # Download
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button("📥 PDF Paper", data=create_pdf(paper_txt), file_name="Paper.pdf", mime="application/pdf")
            with col_d2:
                st.download_button("📥 PDF Answer Key", data=create_pdf(ans_txt), file_name="Answer_Key.pdf", mime="application/pdf")

# Final Call
show_admin_panel()
