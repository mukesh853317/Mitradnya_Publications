import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import datetime
import textwrap

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

def create_pdf(text_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=9)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    clean_text = text_data.encode('latin-1', 'replace').decode('latin-1')
    
    for line in clean_text.split('\n'):
        wrapped_lines = textwrap.wrap(line, width=80, break_long_words=True, replace_whitespace=False)
        
        if not wrapped_lines:
            pdf.ln(5)
            continue
            
        for w_line in wrapped_lines:
            try:
                pdf.multi_cell(0, 5, txt=w_line)
            except Exception:
                pass
                
    out = pdf.output()
    # 🔴 ही ओळ जुन्या आणि नव्या दोन्ही लायब्ररीला सपोर्ट करेल आणि क्रॅश होणार नाही
    if isinstance(out, str):
        return out.encode('latin-1')
    return bytes(out)

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>👨‍🏫 Admin Portal - Paper Generator</h2>", unsafe_allow_html=True)
    st.info("💡 Create fully formatted Question Papers in PDF format. Select the 'Strict Board Paper' tab to generate a perfect 80-marks Maharashtra Board paper with 'OR' options.")
    
    if not FPDF_AVAILABLE:
        st.warning("⚠️ 'fpdf2' library is missing! Papers will be downloaded as TXT. Please add `fpdf2` to your requirements.txt file to enable PDF downloads.")
        
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    except Exception:
        pass
    
    st.write("---")
    
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    obj_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Objectives.csv')
    
    if not os.path.exists(qna_path) or not os.path.exists(obj_path):
        st.error("⚠️ QnA.csv or Objectives.csv files not found in the 'data' folder!")
        return

    qna_df = pd.read_csv(qna_path)
    obj_df = pd.read_csv(obj_path)
    
    qna_df['is_main_question'] = qna_df['Chapter_Name'].notna() & (qna_df['Chapter_Name'].astype(str).str.strip() != '')
    qna_df['Question_ID'] = qna_df['is_main_question'].cumsum()

    if 'Subject' not in qna_df.columns: qna_df['Subject'] = 'BK'
    if 'Subject' not in obj_df.columns: obj_df['Subject'] = 'BK'
    if 'No' in obj_df.columns: obj_df.rename(columns={'No': 'Chapter_Name'}, inplace=True)
    
    qna_df['Subject'] = qna_df['Subject'].ffill().astype(str).str.strip()
    qna_df['Chapter_Name'] = qna_df['Chapter_Name'].ffill().astype(str).str.strip()
    if 'Category' not in qna_df.columns:
        qna_df['Category'] = 'Exercise_Problems'

    obj_df['Subject'] = obj_df['Subject'].astype(str).str.strip()
    obj_df['Chapter_Name'] = obj_df['Chapter_Name'].astype(str).str.strip()

    all_subjects = list(set(qna_df['Subject'].unique()).union(set(obj_df['Subject'].unique())))

    paper_tabs = st.tabs(["🏛️ Strict Board Paper (80 Marks)", "📝 Custom Practice Paper"])
    
    def get_full_q_both(q_id, df):
        group = df[df['Question_ID'] == q_id]
        html = ""
        text = ""
        in_table = False
        for _, r in group.iterrows():
            line = str(r.get('Question_Text', '')).strip()
            if line == 'nan' or not line: continue
            
            if '|' in line:
                if not in_table:
                    html += '<table border="1" width="100%" cellpadding="4" style="border-collapse: collapse;">'
                    in_table = True
                html += "<tr>"
                cols = line.split('|')
                text += " | ".join([c.strip().ljust(15)[:15] for c in cols]) + "\n"
                for cell in cols:
                    if "Total" in line or "Balance" in line:
                        html += f"<td><b>{cell.strip()}</b></td>"
                    else:
                        html += f"<td>{cell.strip()}</td>"
                html += "</tr>"
            else:
                if in_table:
                    html += "</table><br>"
                    in_table = False
                html += f"{line}<br>"
                text += f"{line}\n"
        if in_table:
            html += "</table><br>"
        return html, text
with paper_tabs[1]:
        st.markdown("#### ⚙️ Custom Paper Settings")
        col_h1, col_h2, col_h3 = st.columns(3)
        with col_h1:
            c_sub = st.selectbox("📚 Select Subject:", all_subjects, key="c_sub")
        with col_h2:
            c_branch = st.text_input("🏢 Branch Name:", value="Ambernath", key="c_branch")
        with col_h3:
            c_date = st.date_input("🗓️ Exam Date:", datetime.date.today(), key="c_date")
            
        c_chaps = sorted(list(set(qna_df[qna_df['Subject'] == c_sub]['Chapter_Name'].unique()).union(set(obj_df[obj_df['Subject'] == c_sub]['Chapter_Name'].unique()))))
        c_sel_chaps = st.multiselect("📑 Select Chapters for Custom Test:", c_chaps, default=c_chaps[:1] if c_chaps else None, key="c_chaps")

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            c_mcq = st.number_input("Number of MCQs:", min_value=0, max_value=50, value=10, key="c_mcq")
            c_mcq_m = st.number_input("Marks per MCQ:", min_value=1, max_value=5, value=1, key="c_mcq_m")
        with col_p2:
            c_th = st.number_input("Number of Practical Qs:", min_value=0, max_value=20, value=2, key="c_th")
            c_th_m = st.number_input("Marks per Q:", min_value=1, max_value=20, value=15, key="c_th_m")
        with col_p3:
            c_time = st.text_input("Time:", value="1 Hour", key="c_time")
            c_tot = (c_mcq * c_mcq_m) + (c_th * c_th_m)
            st.markdown(f"<br><h4 style='color: #166534;'>Total Marks: {c_tot}</h4>", unsafe_allow_html=True)
            
        st.write("---")
        
        if 'c_paper_gen' not in st.session_state:
            st.session_state.c_paper_gen = False

        if st.button("🚀 Generate Custom Paper", type="primary", key="c_gen_btn"):
            if not c_sel_chaps:
                st.warning("⚠️ Please select at least one chapter!")
            else:
                with st.spinner("⏳ Generating..."):
                    filtered_obj = obj_df[(obj_df['Subject'] == c_sub) & (obj_df['Chapter_Name'].isin(c_sel_chaps))]
                    final_mcqs = filtered_obj.sample(min(c_mcq, len(filtered_obj))).reset_index(drop=True) if not filtered_obj.empty else pd.DataFrame()
                        
                    main_qna = qna_df[qna_df['is_main_question'] == True]
                    filtered_qna = main_qna[(main_qna['Subject'] == c_sub) & (main_qna['Chapter_Name'].isin(c_sel_chaps)) & (main_qna['Category'] != 'IMP_Proforma')]
                    final_theory = filtered_qna.sample(min(c_th, len(filtered_qna))).reset_index(drop=True) if not filtered_qna.empty else pd.DataFrame()

                    p_html = f"<h2 align='center'>MITRADNYA PUBLICATIONS</h2><hr>"
                    p_html += f"<table width='100%'><tr><td><b>Branch:</b> {c_branch}</td><td align='right'><b>Date:</b> {c_date.strftime('%d-%m-%Y')}</td></tr>"
                    p_html += f"<tr><td><b>Subject:</b> {c_sub}</td><td align='right'><b>Time:</b> {c_time}</td></tr></table><hr>"
                    p_html += f"<h3 align='center'>TOTAL MARKS: {c_tot}</h3><hr><br>"
                    
                    p_txt = f"MITRADNYA PUBLICATIONS\n"
                    p_txt += f"Branch: {c_branch} | Date: {c_date.strftime('%d-%m-%Y')}\n"
                    p_txt += f"Subject: {c_sub} | Time: {c_time}\n"
                    p_txt += f"Total Marks: {c_tot} Marks\n"
                    p_txt += f"Chapters: {', '.join(c_sel_chaps)}\n"
                    p_txt += f"--------------------------------------------------\n\n"
                    
                    if not final_mcqs.empty:
                        p_html += f"<b>Q.1 Choose the correct alternative. [Marks: {c_mcq * c_mcq_m}]</b><br><br>"
                        p_txt += f"Q.1 Choose the correct alternative. [Marks: {c_mcq * c_mcq_m}]\n\n"
                        for idx, row in final_mcqs.iterrows():
                            p_html += f"<b>({idx+1})</b> {row['Question']}<br>&nbsp;&nbsp;&nbsp;A) {row['Option A']} &nbsp;&nbsp; B) {row['Option B']} &nbsp;&nbsp; C) {row['Option C']} &nbsp;&nbsp; D) {row['Option D']}<br><br>"
                            p_txt += f"({idx+1}) {row['Question']}\n    A) {row['Option A']}   B) {row['Option B']}   C) {row['Option C']}   D) {row['Option D']}\n\n"
                    
                    if not final_theory.empty:
                        p_html += f"<b>Q.2 Solve the following problems. [Marks: {c_th * c_th_m}]</b><br><br>"
                        p_txt += f"Q.2 Solve the following problems. [Marks: {c_th * c_th_m}]\n\n"
                        for idx, row in final_theory.iterrows():
                            q_data = get_full_q_both(row['Question_ID'], qna_df)
                            p_html += f"<b>({idx+1})</b> {q_data[0]}<hr><br>"
                            p_txt += f"({idx+1}) {q_data[1]}\n--------------------------------------------------\n\n"

                    st.session_state.c_p_html = p_html
                    st.session_state.c_p_txt = p_txt
                    st.session_state.c_a_html = "<h3 align='center'>Answer key will be available soon.</h3>"
                    st.session_state.c_paper_gen = True
                    st.rerun()

        if st.session_state.get('c_paper_gen'):
            st.markdown("### 🖨️ Custom Paper Preview")
            with st.container(border=True):
                st.markdown(st.session_state.c_p_html, unsafe_allow_html=True)
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if FPDF_AVAILABLE:
                    c_pdf_bytes = create_pdf(st.session_state.c_p_txt)
                    st.download_button("📥 Download Custom PDF", data=c_pdf_bytes, file_name=f"Custom_Paper_{c_sub}.pdf", mime="application/pdf", type="primary", use_container_width=True)
            with col_d2:
                st.download_button("📥 Download Custom HTML", data=st.session_state.c_p_html, file_name=f"Custom_Paper.html", mime="text/html", type="secondary", use_container_width=True)
