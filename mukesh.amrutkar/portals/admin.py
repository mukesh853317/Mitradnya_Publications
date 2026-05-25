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
    # ... (डेटा लोडिंग आणि सिलेक्शन कोड) ...

    # 🔴 इथे चेकबॉक्सेस ॲड करा
    st.markdown("#### 🎯 प्रश्नांचे प्रकार निवडा:")
    c1, c2, c3 = st.columns(3)
    with c1: use_prac = st.checkbox("Practical Problems", value=True)
    with c2: use_short = st.checkbox("Short Notes", value=True)
    with c3: use_theory = st.checkbox("Theory Questions", value=True)
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
                    html += '<table border="1" width="50%" cellpadding="4" style="border-collapse: collapse;">'
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

    # =========================================================
    # TAB 1: STRICT BOARD PAPER (80 MARKS)
    # =========================================================
    with paper_tabs[0]:
        st.markdown("#### 📝 1. Paper Header")
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            board_sub = st.selectbox("📚 Select Subject:", all_subjects, key="board_sub")
        with col_b2:
            board_branch = st.text_input("🏢 Branch Name:", value="Ambernath", key="board_branch")
        with col_b3:
            board_date = st.date_input("🗓️ Exam Date:", datetime.date.today(), key="board_date")

        all_chaps = sorted(list(set(qna_df[qna_df['Subject'] == board_sub]['Chapter_Name'].unique()).union(set(obj_df[obj_df['Subject'] == board_sub]['Chapter_Name'].unique()))))
        
        st.write("---")
        
        if board_sub.strip().upper() in ['BK', 'BOOK KEEPING', 'BOOK-KEEPING', 'BOOK KEEPING & ACCOUNTANCY']:
            st.markdown(f"#### ⚙️ 2. Chapter Assignments (BK Pattern)")
            st.info("Q.1 Objective Questions (15 Marks) will be drawn randomly from the entire syllabus.")
            
            if not all_chaps:
                st.error("No chapters found for this subject.")
            else:
                c1, c2 = st.columns(2)
                with c1:
                    q2_main = st.selectbox("Q.2 Chapter (Single Entry - 8 Marks)", all_chaps, index=0, key="q2_m_bk")
                    q3_main = st.selectbox("Q.3 Chapter (Admission/Retirement/Death - 10 Marks)", all_chaps, index=min(1, len(all_chaps)-1), key="q3_m_bk")
                    q4_main = st.selectbox("Q.4 Chapter (Bills of Exchange - 10 Marks)", all_chaps, index=min(2, len(all_chaps)-1), key="q4_m_bk")
                    q6_main = st.selectbox("Q.6 Chapter (NPO - 12 Marks)", all_chaps, index=min(3, len(all_chaps)-1), key="q6_m_bk")
                with c2:
                    q2_or = st.selectbox("Q.2 OR Chapter (Financial Statements Theory - 8 Marks)", all_chaps, index=min(1, len(all_chaps)-1), key="q2_o_bk")
                    q3_or = st.selectbox("Q.3 OR Chapter (Admission/Retirement/Death - 10 Marks)", all_chaps, index=min(2, len(all_chaps)-1), key="q3_o_bk")
                    q5_main = st.selectbox("Q.5 Chapter (Dissolution - 10 Marks)", all_chaps, index=min(4, len(all_chaps)-1), key="q5_m_bk")
                    q5_or = st.selectbox("Q.5 OR Chapter (Shares/Debentures - 10 Marks)", all_chaps, index=min(5, len(all_chaps)-1), key="q5_o_bk")
                
                q7_main = st.selectbox("Q.7 Chapter (Partnership Final Accounts - 15 Marks)", all_chaps, index=min(6, len(all_chaps)-1), key="q7_m_bk")

                if 'board_paper_generated' not in st.session_state:
                    st.session_state.board_paper_generated = False
                    st.session_state.board_paper_html = ""
                    st.session_state.board_ans_html = ""
                    st.session_state.board_paper_txt = ""

                if st.button("🚀 Generate 80-Marks BK Paper", type="primary", key="gen_board_bk"):
                    with st.spinner("⏳ Compiling BK Board Pattern Paper..."):
                        main_qna_sub = qna_df[(qna_df['Subject'] == board_sub) & (qna_df['is_main_question'] == True)]
                        obj_sub = obj_df[obj_df['Subject'] == board_sub]
                        
                        p_html = f"<h2 align='center'>MITRADNYA PUBLICATIONS</h2><hr>"
                        p_html += f"<table width='100%'><tr><td><b>Branch:</b> {board_branch}</td><td align='right'><b>Date:</b> {board_date.strftime('%d-%m-%Y')}</td></tr>"
                        p_html += f"<tr><td><b>Subject:</b> {board_sub}</td><td align='right'><b>Time:</b> 3 Hours</td></tr></table><hr>"
                        p_html += f"<h3 align='center'>TOTAL MARKS: 80</h3><hr><br>"
                        
                        p_txt = f"MITRADNYA PUBLICATIONS\n"
                        p_txt += f"Branch: {board_branch} | Date: {board_date.strftime('%d-%m-%Y')}\n"
                        p_txt += f"Subject: {board_sub} | Time: 3 Hours\n"
                        p_txt += f"TOTAL MARKS: 80\n"
                        p_txt += f"--------------------------------------------------\n\n"

                        a_html = f"<h2 align='center'>MITRADNYA PUBLICATIONS - ANSWER KEY</h2><hr><br>"

                        def pull_practical_both(chap, n=1, is_theory=False):
                            cat_filter = 'Short_Notes' if is_theory else 'Exercise_Problems'
                            pool = main_qna_sub[(main_qna_sub['Chapter_Name'] == chap) & (main_qna_sub['Category'] == cat_filter)]
                            if pool.empty:
                                pool = main_qna_sub[(main_qna_sub['Chapter_Name'] == chap) & (main_qna_sub['Category'] != 'IMP_Proforma')]
                            if pool.empty: return [("<p>[Question missing]</p>", "[Question missing]")] * n
                            return [get_full_q_both(r['Question_ID'], qna_df) for _, r in pool.sample(min(n, len(pool))).iterrows()]

                        p_html += "<b>Q.1 Attempt any THREE of the following. [15 Marks]</b><br><br>"
                        p_txt += "Q.1 Attempt any THREE of the following. [15 Marks]\n\n"
                        
                        p_html += "<b>(A) Answer in one sentence only. (05 Marks)</b><br>"
                        p_txt += "(A) Answer in one sentence only. (05 Marks)\n"
                        
                        onesent_df = main_qna_sub[main_qna_sub['Category'] == 'One_Sentence']
                        if not onesent_df.empty:
                            for i, (_, row) in enumerate(onesent_df.sample(min(5, len(onesent_df))).iterrows()):
                                p_html += f"&nbsp;&nbsp;&nbsp;{i+1}) {row['Question_Text']}<br>"
                                p_txt += f"   {i+1}) {row['Question_Text']}\n"
                        else: 
                            p_html += "&nbsp;&nbsp;&nbsp;[Questions not available in database]<br>"
                            p_txt += "   [Questions not available in database]\n"
                        p_html += "<br>"
                        p_txt += "\n"
                        
                        p_html += "<b>(B) Write the word/phrase which can substitute each of the following statements. (05 Marks)</b><br>"
                        p_html += "&nbsp;&nbsp;&nbsp;[Provide Word/Phrase questions from database here]<br><br>"
                        p_txt += "(B) Write the word/phrase which can substitute each... (05 Marks)\n   [Provide Word/Phrase questions here]\n\n"
                        
                        p_html += "<b>(C) Select the most appropriate alternative from those given below and rewrite the statement. (05 Marks)</b><br>"
                        p_txt += "(C) Select the most appropriate alternative... (05 Marks)\n"
                        if not obj_sub.empty:
                            for i, (_, row) in enumerate(obj_sub.sample(min(5, len(obj_sub))).iterrows()):
                                p_html += f"&nbsp;&nbsp;&nbsp;{i+1}) {row['Question']}<br>"
                                p_html += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A) {row['Option A']} &nbsp;&nbsp; B) {row['Option B']} &nbsp;&nbsp; C) {row['Option C']} &nbsp;&nbsp; D) {row['Option D']}<br>"
                                p_txt += f"   {i+1}) {row['Question']}\n       A) {row['Option A']}   B) {row['Option B']}   C) {row['Option C']}   D) {row['Option D']}\n"
                                a_html += f"&nbsp;&nbsp;&nbsp;{i+1}) {row['Correct Answer (Full Text)']}<br>"
                        else: 
                            p_html += "&nbsp;&nbsp;&nbsp;[Questions not available in database]<br>"
                            p_txt += "   [Questions not available in database]\n"
                        p_html += "<br>"
                        p_txt += "\n"
                        
                        p_html += "<b>(D) State whether the following statements are 'True' or 'False'. (05 Marks)</b><br>"
                        p_html += "&nbsp;&nbsp;&nbsp;[Provide True/False questions from database here]<br><br>"
                        p_txt += "(D) State whether the following statements are True/False. (05 Marks)\n   [Provide True/False questions here]\n\n"

                        p_html += "<b>(E) Preparation of format of Bill of Exchange. (05 Marks)</b><br>"
                        p_txt += "(E) Preparation of format of Bill of Exchange. (05 Marks)\n"
                        prof_df = main_qna_sub[main_qna_sub['Category'] == 'IMP_Proforma']
                        if not prof_df.empty:
                            prof_row = prof_df.sample(1).iloc[0]
                            p_html += f"&nbsp;&nbsp;&nbsp;1) {prof_row['Question_Text']}<br>"
                            p_txt += f"   1) {prof_row['Question_Text']}\n"
                        else: 
                            p_html += "&nbsp;&nbsp;&nbsp;1) Prepare a standard format of Bill of Exchange.<br>"
                            p_txt += "   1) Prepare a standard format of Bill of Exchange.\n"
                        p_html += "<hr><br>"
                        p_txt += "--------------------------------------------------\n\n"

                        q2 = pull_practical_both(q2_main, 1)[0]
                        p_html += "<b>Q.2 Solve the following Practical Problem on Single Entry System. [08 Marks]</b><br>" + q2[0] + "<br><h3 align='center'>OR</h3><br>"
                        p_txt += "Q.2 Solve the following Practical Problem on Single Entry System. [08 Marks]\n" + q2[1] + "\n\n                   OR\n\n"
                        
                        p_html += "<b>Q.2 Attempt the following Theory questions on Financial Statements. [08 Marks]</b><br>"
                        p_txt += "Q.2 Attempt the following Theory questions on Financial Statements. [08 Marks]\n"
                        th_qs = pull_practical_both(q2_or, 2, is_theory=True)
                        for i, q in enumerate(th_qs): 
                            p_html += f"<b>({i+1})</b> {q[0]} [4 Marks]<br>"
                            p_txt += f"({i+1}) {q[1]} [4 Marks]\n"
                        p_html += "<hr><br>"
                        p_txt += "--------------------------------------------------\n\n"

                        q3_m = pull_practical_both(q3_main, 1)[0]
                        q3_o = pull_practical_both(q3_or, 1)[0]
                        p_html += "<b>Q.3 Practical Problem on Reconstitution of Partnership. [10 Marks]</b><br>" + q3_m[0] + "<br><h3 align='center'>OR</h3><br>"
                        p_html += "<b>Q.3 Practical Problem on Admission/Retirement/Death of Partner. [10 Marks]</b><br>" + q3_o[0] + "<br><hr><br>"
                        p_txt += "Q.3 Practical Problem on Reconstitution of Partnership. [10 Marks]\n" + q3_m[1] + "\n\n                   OR\n\n"
                        p_txt += "Q.3 Practical Problem on Admission/Retirement/Death of Partner. [10 Marks]\n" + q3_o[1] + "\n--------------------------------------------------\n\n"

                        q4 = pull_practical_both(q4_main, 1)[0]
                        p_html += "<b>Q.4 Practical Problem on Bills of Exchange. [10 Marks]</b><br>" + q4[0] + "<br><hr><br>"
                        p_txt += "Q.4 Practical Problem on Bills of Exchange. [10 Marks]\n" + q4[1] + "\n--------------------------------------------------\n\n"

                        q5_m = pull_practical_both(q5_main, 1)[0]
                        q5_o = pull_practical_both(q5_or, 1)[0]
                        p_html += "<b>Q.5 Practical Problem on Dissolution of Partnership firm. [10 Marks]</b><br>" + q5_m[0] + "<br><h3 align='center'>OR</h3><br>"
                        p_html += "<b>Q.5 Practical Problem on Accounting of Shares / Debentures. [10 Marks]</b><br>" + q5_o[0] + "<br><hr><br>"
                        p_txt += "Q.5 Practical Problem on Dissolution of Partnership firm. [10 Marks]\n" + q5_m[1] + "\n\n                   OR\n\n"
                        p_txt += "Q.5 Practical Problem on Accounting of Shares / Debentures. [10 Marks]\n" + q5_o[1] + "\n--------------------------------------------------\n\n"

                        q6 = pull_practical_both(q6_main, 1)[0]
                        p_html += "<b>Q.6 Practical Problem on Not for Profit Concern. [12 Marks]</b><br>" + q6[0] + "<br><hr><br>"
                        p_txt += "Q.6 Practical Problem on Not for Profit Concern. [12 Marks]\n" + q6[1] + "\n--------------------------------------------------\n\n"

                        q7 = pull_practical_both(q7_main, 1)[0]
                        p_html += "<b>Q.7 Practical Problem on Partnership Final Accounts. [15 Marks]</b><br>" + q7[0] + "<br><hr><br>"
                        p_txt += "Q.7 Practical Problem on Partnership Final Accounts. [15 Marks]\n" + q7[1] + "\n==================================================\n\n"
                        
                        st.session_state.board_paper_html = p_html
                        st.session_state.board_paper_txt = p_txt
                        st.session_state.board_ans_html = a_html
                        st.session_state.board_paper_generated = True
                        st.rerun()

        else:
            st.markdown(f"#### ⚙️ 2. Chapter Assignments (Theory Pattern - {board_sub})")
            st.info(f"💡 Since {board_sub} is a theory subject, a standard 80-marks Theory Pattern will be applied.")
            
            if not all_chaps:
                st.error("No chapters found for this subject.")
            else:
                c1, c2 = st.columns(2)
                with c1:
                    t_q2 = st.multiselect("Q.2 Chapters (Explain Terms - 8 Marks)", all_chaps, default=all_chaps[:2] if len(all_chaps)>=2 else all_chaps, key="t_q2")
                    t_q3 = st.multiselect("Q.3 Chapters (Distinguish Between - 12 Marks)", all_chaps, default=all_chaps[:2] if len(all_chaps)>=2 else all_chaps, key="t_q3")
                    t_q4 = st.multiselect("Q.4 Chapters (Answer in Brief - 12 Marks)", all_chaps, default=all_chaps[:2] if len(all_chaps)>=2 else all_chaps, key="t_q4")
                with c2:
                    t_q5 = st.multiselect("Q.5 Chapters (Justify - 8 Marks)", all_chaps, default=all_chaps[:2] if len(all_chaps)>=2 else all_chaps, key="t_q5")
                    t_q6 = st.multiselect("Q.6 Chapters (Attempt the Following - 10 Marks)", all_chaps, default=all_chaps[:2] if len(all_chaps)>=2 else all_chaps, key="t_q6")
                    t_q7 = st.multiselect("Q.7 Chapters (Long Answers - 10 Marks)", all_chaps, default=all_chaps[:2] if len(all_chaps)>=2 else all_chaps, key="t_q7")

                if 'board_paper_generated' not in st.session_state:
                    st.session_state.board_paper_generated = False
                    st.session_state.board_paper_html = ""
                    st.session_state.board_paper_txt = ""
                    st.session_state.board_ans_html = ""

                if st.button(f"🚀 Generate 80-Marks {board_sub} Paper", type="primary", key="gen_board_other"):
                    with st.spinner(f"⏳ Compiling {board_sub} Board Pattern Paper..."):
                        main_qna_sub = qna_df[(qna_df['Subject'] == board_sub) & (qna_df['is_main_question'] == True)]
                        obj_sub = obj_df[obj_df['Subject'] == board_sub]
                        
                        p_html = f"<h2 align='center'>MITRADNYA PUBLICATIONS</h2><hr>"
                        p_html += f"<table width='100%'><tr><td><b>Branch:</b> {board_branch}</td><td align='right'><b>Date:</b> {board_date.strftime('%d-%m-%Y')}</td></tr>"
                        p_html += f"<tr><td><b>Subject:</b> {board_sub}</td><td align='right'><b>Time:</b> 3 Hours</td></tr></table><hr>"
                        p_html += f"<h3 align='center'>TOTAL MARKS: 80</h3><hr><br>"
                        
                        p_txt = f"MITRADNYA PUBLICATIONS\n"
                        p_txt += f"Branch: {board_branch} | Date: {board_date.strftime('%d-%m-%Y')}\n"
                        p_txt += f"Subject: {board_sub} | Time: 3 Hours\n"
                        p_txt += f"TOTAL MARKS: 80\n"
                        p_txt += f"--------------------------------------------------\n\n"

                        a_html = f"<h2 align='center'>MITRADNYA PUBLICATIONS - ANSWER KEY</h2><hr><br>"

                        def pull_theory_both(chaps, n=1):
                            pool = main_qna_sub[main_qna_sub['Chapter_Name'].isin(chaps)]
                            if pool.empty: return [("<p>[Question missing]</p>", "[Question missing]")] * n
                            return [get_full_q_both(r['Question_ID'], qna_df) for _, r in pool.sample(min(n, len(pool)), replace=True).iterrows()]

                        p_html += "<b>Q.1 Objective Questions. [20 Marks]</b><br><br>"
                        p_txt += "Q.1 Objective Questions. [20 Marks]\n\n"
                        
                        p_html += "<b>(A) Select the correct option and rewrite the sentence. (05 Marks)</b><br>"
                        p_txt += "(A) Select the correct option and rewrite the sentence. (05 Marks)\n"
                        if not obj_sub.empty:
                            for i, (_, row) in enumerate(obj_sub.sample(min(5, len(obj_sub))).iterrows()):
                                p_html += f"&nbsp;&nbsp;&nbsp;{i+1}) {row['Question']}<br>"
                                p_html += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A) {row['Option A']} &nbsp;&nbsp; B) {row['Option B']} &nbsp;&nbsp; C) {row['Option C']} &nbsp;&nbsp; D) {row['Option D']}<br>"
                                p_txt += f"   {i+1}) {row['Question']}\n       A) {row['Option A']}   B) {row['Option B']}   C) {row['Option C']}   D) {row['Option D']}\n"
                                a_html += f"&nbsp;&nbsp;&nbsp;{i+1}) {row['Correct Answer (Full Text)']}<br>"
                        else: 
                            p_html += "&nbsp;&nbsp;&nbsp;[Questions not available in database]<br>"
                            p_txt += "   [Questions not available in database]\n"
                        p_html += "<hr><br>"
                        p_txt += "--------------------------------------------------\n\n"

                        p_html += "<b>Q.2 Explain the following terms / concepts (Any 4). [08 Marks]</b><br>"
                        p_txt += "Q.2 Explain the following terms / concepts (Any 4). [08 Marks]\n"
                        th_qs = pull_theory_both(t_q2, 6)
                        for i, q in enumerate(th_qs): 
                            p_html += f"<b>({i+1})</b> {q[0]}<br>"
                            p_txt += f"({i+1}) {q[1]}\n"
                        p_html += "<hr><br>"
                        p_txt += "--------------------------------------------------\n\n"

                        p_html += "<b>Q.3 Distinguish Between (Any 3). [12 Marks]</b><br>"
                        p_txt += "Q.3 Distinguish Between (Any 3). [12 Marks]\n"
                        th_qs = pull_theory_both(t_q3, 5)
                        for i, q in enumerate(th_qs): 
                            p_html += f"<b>({i+1})</b> {q[0]}<br>"
                            p_txt += f"({i+1}) {q[1]}\n"
                        p_html += "<hr><br>"
                        p_txt += "--------------------------------------------------\n\n"

                        p_html += "<b>Q.4 Answer in Brief (Any 3). [12 Marks]</b><br>"
                        p_txt += "Q.4 Answer in Brief (Any 3). [12 Marks]\n"
                        th_qs = pull_theory_both(t_q4, 5)
                        for i, q in enumerate(th_qs): 
                            p_html += f"<b>({i+1})</b> {q[0]}<br>"
                            p_txt += f"({i+1}) {q[1]}\n"
                        p_html += "<hr><br>"
                        p_txt += "--------------------------------------------------\n\n"
                        
                        p_html += "<b>Q.5 Justify the following statements (Any 2). [08 Marks]</b><br>"
                        p_txt += "Q.5 Justify the following statements (Any 2). [08 Marks]\n"
                        th_qs = pull_theory_both(t_q5, 4)
                        for i, q in enumerate(th_qs): 
                            p_html += f"<b>({i+1})</b> {q[0]}<br>"
                            p_txt += f"({i+1}) {q[1]}\n"
                        p_html += "<hr><br>"
                        p_txt += "--------------------------------------------------\n\n"

                        p_html += "<b>Q.6 Attempt the following (Any 2). [10 Marks]</b><br>"
                        p_txt += "Q.6 Attempt the following (Any 2). [10 Marks]\n"
                        th_qs = pull_theory_both(t_q6, 4)
                        for i, q in enumerate(th_qs): 
                            p_html += f"<b>({i+1})</b> {q[0]}<br>"
                            p_txt += f"({i+1}) {q[1]}\n"
                        p_html += "<hr><br>"
                        p_txt += "--------------------------------------------------\n\n"
                        
                        p_html += "<b>Q.7 Answer the following in detail (Any 1). [10 Marks]</b><br>"
                        p_txt += "Q.7 Answer the following in detail (Any 1). [10 Marks]\n"
                        th_qs = pull_theory_both(t_q7, 3)
                        for i, q in enumerate(th_qs): 
                            p_html += f"<b>({i+1})</b> {q[0]}<br>"
                            p_txt += f"({i+1}) {q[1]}\n"
                        p_html += "<hr><br>"
                        p_txt += "==================================================\n\n"

                        st.session_state.board_paper_html = p_html
                        st.session_state.board_paper_txt = p_txt
                        st.session_state.board_ans_html = a_html
                        st.session_state.board_paper_generated = True
                        st.rerun()

        if st.session_state.get('board_paper_generated'):
            st.markdown("### 🖨️ Board Paper Preview & Download")
            st.success("✅ 80-Marks Board Paper Generated! Tables are formatted correctly.")
            
            p_tabs = st.tabs(["📄 Question Paper", "📝 Answer Key & AI Reference"])
            with p_tabs[0]:
                with st.container(border=True):
                    st.markdown(st.session_state.board_paper_html, unsafe_allow_html=True)
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if FPDF_AVAILABLE:
                        pdf_bytes = create_pdf(st.session_state.board_paper_txt)
                        st.download_button("📥 Download PDF", data=pdf_bytes, file_name=f"Board_80_Marks_{board_sub}.pdf", mime="application/pdf", type="primary", use_container_width=True)
                with col_btn2:
                    st.download_button("📥 Download HTML (For Print)", data=st.session_state.board_paper_html, file_name=f"Board_80_Marks_{board_sub}.html", mime="text/html", type="secondary", use_container_width=True)

            with p_tabs[1]:
                with st.container(border=True):
                    st.markdown(st.session_state.board_ans_html, unsafe_allow_html=True)
                
                col_ab1, col_ab2 = st.columns(2)
                with col_ab1:
                    st.download_button("📥 Download Answer HTML", data=st.session_state.board_ans_html, file_name=f"Board_80_Ans_Key_{board_sub}.html", mime="text/html", type="secondary", use_container_width=True)
                
                st.write("---")
                if st.button("🤖 Generate AI Teacher's Solution for Board Paper", key="ai_board"):
                    with st.spinner("⏳ AI is calculating solutions..."):
                        try:
                            model = genai.GenerativeModel('gemini-3.5-flash')
                            prompt = f"Provide a complete, step-by-step solution for this board exam paper (Use clean HTML tables for accounts):\n\n{st.session_state.board_paper_html}"
                            response = model.generate_content(prompt, stream=True, request_options={"timeout": 600})
                            res_box = st.empty()
                            full_text = ""
                            for chunk in response:
                                full_text += chunk.text
                                res_box.markdown(full_text + " ▌")
                            res_box.markdown(full_text)
                        except Exception as e:
                            st.error(f"AI Error: {e}")

    # =========================================================
    # TAB 2: CUSTOM PRACTICE PAPER
    # =========================================================
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
