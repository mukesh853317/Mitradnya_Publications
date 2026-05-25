import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>👨‍🏫 Admin Portal - Paper & Solution Generator</h2>", unsafe_allow_html=True)
    st.info("💡 Create Test Papers on One Click! Choose the Subject, Lessons, Number of Questions & Generate Paper.")
    
    # AI Setup
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    except Exception:
        pass
    
    st.write("---")
    
    # 1. डेटा लोड करणे
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    obj_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Objectives.csv')
    
    if not os.path.exists(qna_path) or not os.path.exists(obj_path):
        st.error("⚠️ Data files (QnA.csv or Objectives.csv) are missing in the 'data' folder!")
        return

    qna_df = pd.read_csv(qna_path)
    obj_df = pd.read_csv(obj_path)
    
    # QnA मध्ये is_main_question तयार करणे
    qna_df['is_main_question'] = qna_df['Chapter_Name'].notna() & (qna_df['Chapter_Name'].astype(str).str.strip() != '')
    qna_df['Question_ID'] = qna_df['is_main_question'].cumsum()

    # डेटा क्लीनिंग
    if 'Subject' not in qna_df.columns: qna_df['Subject'] = 'BK'
    if 'Subject' not in obj_df.columns: obj_df['Subject'] = 'BK'
    if 'No' in obj_df.columns: obj_df.rename(columns={'No': 'Chapter_Name'}, inplace=True)
    
    qna_df['Subject'] = qna_df['Subject'].ffill().astype(str).str.strip()
    qna_df['Chapter_Name'] = qna_df['Chapter_Name'].ffill().astype(str).str.strip()
    if 'Category' in qna_df.columns:
        qna_df['Category'] = qna_df['Category'].ffill()
    else:
        qna_df['Category'] = 'Exercise_Problems'

    obj_df['Subject'] = obj_df['Subject'].astype(str).str.strip()
    obj_df['Chapter_Name'] = obj_df['Chapter_Name'].astype(str).str.strip()

    all_subjects = list(set(qna_df['Subject'].unique()).union(set(obj_df['Subject'].unique())))
    
    # 2. पेपर सेटिंग UI
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_subject = st.selectbox("📚 Select Subject:", all_subjects)
    
    chap_qna = qna_df[qna_df['Subject'] == selected_subject]['Chapter_Name'].unique().tolist()
    chap_obj = obj_df[obj_df['Subject'] == selected_subject]['Chapter_Name'].unique().tolist()
    all_chapters = list(set(chap_qna).union(set(chap_obj)))
    all_chapters.sort()

    with col2:
        selected_chapters = st.multiselect("📑 Select Chapters for Test:", all_chapters, default=all_chapters[:1] if all_chapters else None)

    st.markdown("#### ⚙️ Set Paper Pattern")
    col3, col4 = st.columns(2)
    with col3:
        num_mcq = st.number_input("Number of MCQs (1 Mark each):", min_value=0, max_value=50, value=10, step=1)
    with col4:
        num_theory = st.number_input("Number of Theory/Practical Questions:", min_value=0, max_value=20, value=5, step=1)
        
    st.write("---")
    
    # 3. Session State Initialization
    if 'paper_generated' not in st.session_state:
        st.session_state.paper_generated = False
    
    # पेपर जनरेट करणे
    if st.button("🚀 Generate Question Paper & Answer Key", type="primary"):
        if not selected_chapters:
            st.warning("⚠️ Please select at least one chapter!")
            return
            
        with st.spinner("⏳ Generating..."):
            filtered_obj = obj_df[(obj_df['Subject'] == selected_subject) & (obj_df['Chapter_Name'].isin(selected_chapters))]
            if not filtered_obj.empty:
                take_mcq = min(num_mcq, len(filtered_obj))
                final_mcqs = filtered_obj.sample(n=take_mcq).reset_index(drop=True)
            else:
                final_mcqs = pd.DataFrame()
                
            main_qna = qna_df[qna_df['is_main_question'] == True]
            filtered_qna = main_qna[(main_qna['Subject'] == selected_subject) & (main_qna['Chapter_Name'].isin(selected_chapters)) & (main_qna['Category'] != 'IMP_Proforma')]
            
            if not filtered_qna.empty:
                take_theory = min(num_theory, len(filtered_qna))
                final_theory = filtered_qna.sample(n=take_theory).reset_index(drop=True)
            else:
                final_theory = pd.DataFrame()

            # Save to session state
            st.session_state.final_mcqs = final_mcqs
            st.session_state.final_theory = final_theory
            st.session_state.sel_sub = selected_subject
            st.session_state.sel_chaps = selected_chapters
            st.session_state.full_qna_df = qna_df
            st.session_state.paper_generated = True
            st.rerun()

    # ==============================================================
    # 4. पेपर आणि उत्तरे दाखवणे (Tabs मध्ये)
    # ==============================================================
    if st.session_state.paper_generated:
        out_tabs = st.tabs(["📄 Question Paper", "📝 Answer Key & Solutions"])
        
        final_mcqs = st.session_state.final_mcqs
        final_theory = st.session_state.final_theory
        sel_sub = st.session_state.sel_sub
        sel_chaps = st.session_state.sel_chaps
        qna_df_full = st.session_state.full_qna_df
        
        # ----------------------------------------------------
        # TAB 1: QUESTION PAPER
        # ----------------------------------------------------
        with out_tabs[0]:
            st.success("✅ Paper Generated Successfully!")
            
            # --- हेडर आणि लोगो ---
            col_logo, col_title = st.columns([1, 4])
            with col_logo:
                logo_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'images', 'logo.png')
                if os.path.exists(logo_path):
                    st.image(logo_path, width=100)
                else:
                    st.markdown("🏢", unsafe_allow_html=True) # Placeholder icon
            with col_title:
                st.markdown("<h2 style='color: #1e3a8a; margin-bottom: 0;'>MITRADNYA PUBLICATIONS</h2>", unsafe_allow_html=True)
                st.markdown(f"**Subject:** {sel_sub} | **Chapters:** {', '.join(sel_chaps)}")
            
            st.markdown("<hr style='border: 2px solid #1e3a8a;'>", unsafe_allow_html=True)
            
            # Text file content builder (with proper line breaks)
            txt_content = "========================================\r\n"
            txt_content += "        MITRADNYA PUBLICATIONS\r\n"
            txt_content += "========================================\r\n"
            txt_content += f"Subject: {sel_sub}\r\n"
            txt_content += f"Chapters: {', '.join(sel_chaps)}\r\n"
            txt_content += "----------------------------------------\r\n\r\n"

            with st.container(border=True):
                # Section A: MCQs
                if not final_mcqs.empty:
                    st.markdown("#### Q.1 Choose the correct alternative and rewrite the sentence:")
                    txt_content += "Q.1 Choose the correct alternative and rewrite the sentence:\r\n\r\n"
                    
                    for idx, row in final_mcqs.iterrows():
                        q_text = f"**{idx+1}.** {row['Question']}"
                        opts = f"A) {row['Option A']} &nbsp;&nbsp; B) {row['Option B']} &nbsp;&nbsp; C) {row['Option C']} &nbsp;&nbsp; D) {row['Option D']}"
                        
                        st.markdown(q_text)
                        st.markdown(opts, unsafe_allow_html=True)
                        st.write("")
                        
                        txt_content += f"{idx+1}. {row['Question']}\r\n"
                        txt_content += f"A) {row['Option A']}   B) {row['Option B']}   C) {row['Option C']}   D) {row['Option D']}\r\n\r\n"
                
                # Section B: Theory / Practical
                if not final_theory.empty:
                    st.markdown("#### Q.2 Solve the following questions:")
                    txt_content += "Q.2 Solve the following questions:\r\n\r\n"
                    
                    for idx, row in final_theory.iterrows():
                        q_id = row['Question_ID']
                        group = qna_df_full[qna_df_full['Question_ID'] == q_id]
                        full_q_text = "\n".join([str(r.get('Question_Text', '')).strip() for _, r in group.iterrows() if str(r.get('Question_Text', '')).strip() != 'nan'])
                        
                        st.markdown(f"**{idx+1}.**")
                        txt_content += f"{idx+1}. "
                        
                        # 🔴 टेबल रेंडरिंग लॉजिक (Student Portal सारखे)
                        table_data = []
                        for line in full_q_text.split('\n'):
                            if '|' in line:
                                table_data.append([col.strip() for col in line.split('|')])
                                # Text file formatting for tables (simple padding)
                                txt_content += line.replace('|', ' | ') + "\r\n"
                            else:
                                if table_data:
                                    html_table = "<table style='width:100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom:10px;'>"
                                    for r_idx, t_row in enumerate(table_data):
                                        html_table += "<tr>"
                                        for col in t_row:
                                            if r_idx == 0: html_table += f"<th style='border: 1px solid #ddd; padding: 8px; text-align: center; background-color: #f2f2f2;'>{col}</th>"
                                            else: html_table += f"<td style='border: 1px solid #ddd; padding: 8px;'>{col}</td>"
                                        html_table += "</tr>"
                                    html_table += "</table>"
                                    st.markdown(html_table, unsafe_allow_html=True)
                                    table_data = []
                                
                                if line:
                                    st.markdown(line)
                                    txt_content += line + "\r\n"
                                    
                        # उरलेला टेबल
                        if table_data:
                            html_table = "<table style='width:100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom:10px;'>"
                            for r_idx, t_row in enumerate(table_data):
                                html_table += "<tr>"
                                for col in t_row:
                                    if r_idx == 0: html_table += f"<th style='border: 1px solid #ddd; padding: 8px; text-align: center; background-color: #f2f2f2;'>{col}</th>"
                                    else: html_table += f"<td style='border: 1px solid #ddd; padding: 8px;'>{col}</td>"
                                html_table += "</tr>"
                            html_table += "</table>"
                            st.markdown(html_table, unsafe_allow_html=True)
                        
                        st.write("---")
                        txt_content += "\r\n----------------------------------------\r\n\r\n"

            st.write("")
            st.download_button(
                label="📥 Download Paper (.txt)",
                data=txt_content,
                file_name=f"{sel_sub}_Question_Paper.txt",
                mime="text/plain",
                type="primary"
            )

        # ----------------------------------------------------
        # TAB 2: ANSWER KEY & SOLUTIONS
        # ----------------------------------------------------
        with out_tabs[1]:
            st.markdown("<h3 style='color: #166534;'>📝 Official Answer Key & Solutions</h3>", unsafe_allow_html=True)
            
            ans_content = "========================================\r\n"
            ans_content += "       ANSWER KEY & SOLUTIONS\r\n"
            ans_content += "========================================\r\n\r\n"

            with st.container(border=True):
                if not final_mcqs.empty:
                    st.markdown("#### Q.1 MCQ Answers:")
                    ans_content += "Q.1 MCQ Answers:\r\n"
                    for idx, row in final_mcqs.iterrows():
                        ans_text = f"**{idx+1}.** {row['Correct Answer (Full Text)']}"
                        st.success(ans_text)
                        ans_content += f"{idx+1}. {row['Correct Answer (Full Text)']}\r\n"
                    st.write("---")
                    ans_content += "\r\n----------------------------------------\r\n\r\n"

                if not final_theory.empty:
                    st.markdown("#### Q.2 Practical / Theory Solutions:")
                    ans_content += "Q.2 Practical / Theory Solutions:\r\n(Refer to AI Generated Solutions for detailed steps)\r\n\r\n"
                    
                    for idx, row in final_theory.iterrows():
                        q_id = row['Question_ID']
                        group = qna_df_full[qna_df_full['Question_ID'] == q_id]
                        full_q_text = "\n".join([str(r.get('Question_Text', '')).strip() for _, r in group.iterrows() if str(r.get('Question_Text', '')).strip() != 'nan'])
                        
                        with st.expander(f"View Question {idx+1}"):
                            st.text(full_q_text[:200] + "...")
                            
                        # AI Solution Button
                        if st.button(f"🧠 Generate Solution for Q.{idx+1}", key=f"ai_ans_{q_id}"):
                            with st.spinner("⏳ Generating Detailed Solution..."):
                                try:
                                    model = genai.GenerativeModel('gemini-3.5-flash')
                                    prompt = f"Solve this accountancy/commerce problem in detail step-by-step for a teacher's answer key. Subject: {sel_sub}.\n\n{full_q_text}"
                                    response = model.generate_content(prompt, stream=True, request_options={"timeout": 600})
                                    
                                    st.markdown(f"**Solution for Q.{idx+1}:**")
                                    res_box = st.empty()
                                    full_text = ""
                                    for chunk in response:
                                        full_text += chunk.text
                                        res_box.markdown(full_text + " ▌")
                                    res_box.markdown(full_text)
                                except Exception as e:
                                    st.error(f"AI Error: {e}")
                                    
                        st.write("")

            st.write("")
            st.download_button(
                label="📥 Download Answer Key (.txt)",
                data=ans_content,
                file_name=f"{sel_sub}_Answer_Key.txt",
                mime="text/plain",
                type="primary"
            )
