import streamlit as st

import pandas as pd

import os

import google.generativeai as genai

import datetime



def show_admin_panel():

    st.markdown("<h2 style='color: #1e3a8a;'>👨‍🏫 Admin Portal - Advanced Board Paper Generator</h2>", unsafe_allow_html=True)

    st.info("💡 Create beautiful question papers with Board Pattern Marks, Date, and Branch.")

    

    # AI Setup

    try:

        api_key = st.secrets["GOOGLE_API_KEY"]

        genai.configure(api_key=api_key)

    except Exception:

        pass

    

    st.write("---")

    

    # 1. Load Data

    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')

    obj_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Objectives.csv')

    

    if not os.path.exists(qna_path) or not os.path.exists(obj_path):

        st.error("⚠️ QnA.csv or Objectives.csv files not found in the 'data' folder!")

        return



    qna_df = pd.read_csv(qna_path)

    obj_df = pd.read_csv(obj_path)

    

    # QnA is_main_question setup

    qna_df['is_main_question'] = qna_df['Chapter_Name'].notna() & (qna_df['Chapter_Name'].astype(str).str.strip() != '')

    qna_df['Question_ID'] = qna_df['is_main_question'].cumsum()



    # Data Cleaning

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

    

    # 2. Header and Pattern Settings UI

    st.markdown("#### 📝 1. Header Information")

    col_h1, col_h2, col_h3 = st.columns(3)

    with col_h1:

        selected_subject = st.selectbox("📚 Select Subject:", all_subjects, key="admin_sub_select")

    with col_h2:

        branch_name = st.text_input("🏢 Enter Branch Name:", value="Ambernath")

    with col_h3:

        exam_date = st.date_input("🗓️ Select Exam Date:", datetime.date.today())

        

    chap_qna = qna_df[qna_df['Subject'] == selected_subject]['Chapter_Name'].unique().tolist()

    chap_obj = obj_df[obj_df['Subject'] == selected_subject]['Chapter_Name'].unique().tolist()

    all_chapters = list(set(chap_qna).union(set(chap_obj)))

    all_chapters.sort()

    

    selected_chapters = st.multiselect("📑 Select Chapters for Test:", all_chapters, default=all_chapters[:1] if all_chapters else None)



    st.markdown("#### ⚙️ 2. Board Paper Pattern & Marks Settings")

    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:

        num_mcq = st.number_input("Number of MCQs:", min_value=0, max_value=50, value=10, step=1)

        mcq_marks = st.number_input("Marks per MCQ:", min_value=1, max_value=5, value=1, step=1)

    with col_p2:

        num_theory = st.number_input("Number of Practical/Theory Qs:", min_value=0, max_value=20, value=2, step=1)

        theory_marks = st.number_input("Marks per Practical Q:", min_value=1, max_value=20, value=15, step=1)

    with col_p3:

        total_time = st.text_input("Exam Duration (Time):", value="2 Hours")

        calculated_total = (num_mcq * mcq_marks) + (num_theory * theory_marks)

        st.markdown(f"<br><h4 style='color: #166534;'>Total Marks: {calculated_total}</h4>", unsafe_allow_html=True)

        

    st.write("---")

    

    if 'admin_paper_generated' not in st.session_state:

        st.session_state.admin_paper_generated = False

        st.session_state.paper_raw_text = ""

        st.session_state.ans_raw_text = ""



    if st.button("🚀 Generate Board Question Paper", type="primary", key="gen_board_paper_btn"):

        if not selected_chapters:

            st.warning("⚠️ Please select at least one chapter!")

            return

            

        with st.spinner("⏳ Generating Board Pattern Paper..."):

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



            formatted_date = exam_date.strftime('%d-%m-%Y')

            

            # ---------------- BUILD PAPER TEXT ----------------

            p_text = f"========================================\n"

            p_text += f"        MITRADNYA PUBLICATIONS\n"

            p_text += f"========================================\n"

            p_text += f"Branch: {branch_name}          Date: {formatted_date}\n"

            p_text += f"Subject: {selected_subject}             Time: {total_time}\n"

            p_text += f"Total Marks: {calculated_total} Marks\n"

            p_text += f"Chapters: {', '.join(selected_chapters)}\n"

            p_text += f"----------------------------------------\n\n"

            

            if not final_mcqs.empty:

                p_text += f"Q.1 Choose the correct alternative and rewrite the sentence. [Marks: {num_mcq * mcq_marks}]\n\n"

                for idx, row in final_mcqs.iterrows():

                    p_text += f"({idx+1}) {row['Question']}\n"

                    p_text += f"    A) {row['Option A']}   B) {row['Option B']}   C) {row['Option C']}   D) {row['Option D']}\n\n"

            

            if not final_theory.empty:

                p_text += f"Q.2 Solve the following Practical / Theory problems. [Marks: {num_theory * theory_marks} (Each carries {theory_marks} Marks)]\n\n"

                for idx, row in final_theory.iterrows():

                    q_id = row['Question_ID']

                    group = qna_df[qna_df['Question_ID'] == q_id]

                    full_q_text = "\n".join([str(r.get('Question_Text', '')).strip() for _, r in group.iterrows() if str(r.get('Question_Text', '')).strip() != 'nan'])

                    p_text += f"({idx+1}) {full_q_text}\n"

                    p_text += f"----------------------------------------\n\n"



            # ---------------- BUILD ANSWER KEY TEXT ----------------

            a_text = f"========================================\n"

            a_text += f"    MITRADNYA PUBLICATIONS - ANSWER KEY\n"

            a_text += f"========================================\n"

            a_text += f"Subject: {selected_subject} | Date: {formatted_date}\n\n"

            

            if not final_mcqs.empty:

                a_text += f"--- Q.1 MCQ ANSWERS ---\n"

                for idx, row in final_mcqs.iterrows():

                    a_text += f"{idx+1}. Correct Answer: {row['Correct Answer (Full Text)']}\n"

                a_text += f"\n"

            

            if not final_theory.empty:

                a_text += f"--- Q.2 PRACTICAL SOLUTIONS ---\n"

                for idx, row in final_theory.iterrows():

                    a_text += f"Question {idx+1} Solution Hint: Refer to AI Solutions or textbook answers.\n\n"



            st.session_state.paper_raw_text = p_text

            st.session_state.ans_raw_text = a_text

            st.session_state.admin_paper_generated = True

            st.rerun()



    # ==============================================================

    # 3. Print Preview & Download Section (Cleaned UI)

    # ==============================================================

    if st.session_state.admin_paper_generated:

        st.markdown("### 🖨️ 3. Print Preview & Download")

        

        out_tabs = st.tabs(["📄 Question Paper Preview", "📝 Answer Key & AI Solutions"])

        

        # TAB 1: QUESTION PAPER

        with out_tabs[0]:

            st.success("✅ Paper generated successfully! Click download below to save it.")

            

            # Clean Print Preview instead of text area

            with st.container(border=True):

                st.markdown(f"```text\n{st.session_state.paper_raw_text}\n```")

            

            st.write("---")

            st.download_button(

                label="📥 Download Question Paper (.txt)",

                data=st.session_state.paper_raw_text,

                file_name=f"{selected_subject}_Board_Exam_Paper.txt",

                mime="text/plain",

                type="primary",

                use_container_width=True

            )



        # TAB 2: ANSWER KEY & AI SOLUTIONS

        with out_tabs[1]:

            with st.container(border=True):

                st.markdown(f"```text\n{st.session_state.ans_raw_text}\n```")

                

            st.write("---")

            st.download_button(

                label="📥 Download Answer Key (.txt)",

                data=st.session_state.ans_raw_text,

                file_name=f"{selected_subject}_Answer_Key.txt",

                mime="text/plain",

                type="primary",

                use_container_width=True

            )

            

            st.write("---")

            st.markdown("#### 🧠 Generate Detailed AI Solutions for Teachers:")

            

            if st.button("🤖 Generate Full Paper Solution via Gemini AI", type="secondary"):

                with st.spinner("⏳ Gemini AI is solving the entire paper..."):

                    try:

                        model = genai.GenerativeModel('gemini-3.5-flash')

                        prompt = f"Solve this complete commerce question paper step-by-step with accounting formats, adjustments, and explanations for a teacher's answer key:\n\n{st.session_state.paper_raw_text}"

                        response = model.generate_content(prompt, stream=True, request_options={"timeout": 600})

                        

                        st.markdown("### 📝 AI Generated Model Solution:")

                        res_box = st.empty()

                        full_text = ""

                        for chunk in response:

                            full_text += chunk.text

                            res_box.markdown(full_text + " ▌")

                        res_box.markdown(full_text)

                    except Exception as e:

                        st.error(f"AI Error: {e}") 

