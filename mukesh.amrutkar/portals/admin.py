import streamlit as st
import pandas as pd
import os
import random

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>👨‍🏫 Admin Portal - Automatic Paper Generator</h2>", unsafe_allow_html=True)
    st.info("💡 एका क्लिकवर टेस्ट पेपर तयार करा! विषय, धडे आणि प्रश्नांची संख्या निवडा आणि पेपर जनरेट करा.")
    
    st.write("---")
    
    # 1. डेटा लोड करणे
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    obj_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Objectives.csv')
    
    if not os.path.exists(qna_path) or not os.path.exists(obj_path):
        st.error("⚠️ Data files (QnA.csv or Objectives.csv) are missing in the 'data' folder!")
        return

    qna_df = pd.read_csv(qna_path)
    obj_df = pd.read_csv(obj_path)
    
    # डेटा क्लीनिंग
    if 'Subject' not in qna_df.columns: qna_df['Subject'] = 'BK'
    if 'Subject' not in obj_df.columns: obj_df['Subject'] = 'BK'
    if 'No' in obj_df.columns: obj_df.rename(columns={'No': 'Chapter_Name'}, inplace=True)
    
    qna_df['Subject'] = qna_df['Subject'].ffill().astype(str).str.strip()
    qna_df['Chapter_Name'] = qna_df['Chapter_Name'].ffill().astype(str).str.strip()
    obj_df['Subject'] = obj_df['Subject'].astype(str).str.strip()
    obj_df['Chapter_Name'] = obj_df['Chapter_Name'].astype(str).str.strip()

    all_subjects = list(set(qna_df['Subject'].unique()).union(set(obj_df['Subject'].unique())))
    
    # 2. पेपर सेटिंग UI
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_subject = st.selectbox("📚 Select Subject:", all_subjects)
    
    # निवडलेल्या विषयानुसार धडे काढणे
    chap_qna = qna_df[qna_df['Subject'] == selected_subject]['Chapter_Name'].unique().tolist()
    chap_obj = obj_df[obj_df['Subject'] == selected_subject]['Chapter_Name'].unique().tolist()
    all_chapters = list(set(chap_qna).union(set(chap_obj)))
    all_chapters.sort()

    with col2:
        # 🔴 सर्वात भारी फीचर: एकापेक्षा जास्त धडे निवडण्याची सोय (Multi-select)
        selected_chapters = st.multiselect("📑 Select Chapters for Test:", all_chapters, default=all_chapters[:1] if all_chapters else None)

    st.markdown("#### ⚙️ Set Paper Pattern")
    col3, col4 = st.columns(2)
    with col3:
        num_mcq = st.number_input("Number of MCQs (1 Mark each):", min_value=0, max_value=50, value=10, step=1)
    with col4:
        num_theory = st.number_input("Number of Theory/Practical Questions:", min_value=0, max_value=20, value=5, step=1)
        
    st.write("---")
    
    # 3. पेपर जनरेट करणे
    if st.button("🚀 Generate Question Paper", type="primary"):
        if not selected_chapters:
            st.warning("⚠️ Please select at least one chapter!")
            return
            
        with st.spinner("⏳ Generating random question paper..."):
            # ऑब्जेक्टिव्ह प्रश्न निवडणे
            filtered_obj = obj_df[(obj_df['Subject'] == selected_subject) & (obj_df['Chapter_Name'].isin(selected_chapters))]
            if not filtered_obj.empty:
                available_mcqs = len(filtered_obj)
                take_mcq = min(num_mcq, available_mcqs)
                final_mcqs = filtered_obj.sample(n=take_mcq).reset_index(drop=True)
            else:
                final_mcqs = pd.DataFrame()
                
            # थिअरी प्रश्न निवडणे (QnA मधून)
            # फक्त मुख्य प्रश्न घेऊया
            main_qna = qna_df[qna_df['is_main_question'] == True]
            filtered_qna = main_qna[(main_qna['Subject'] == selected_subject) & (main_qna['Chapter_Name'].isin(selected_chapters)) & (main_qna['Category'] != 'IMP_Proforma')]
            if not filtered_qna.empty:
                available_theory = len(filtered_qna)
                take_theory = min(num_theory, available_theory)
                final_theory = filtered_qna.sample(n=take_theory).reset_index(drop=True)
            else:
                final_theory = pd.DataFrame()

            # 4. पेपर डिस्प्ले करणे
            st.success("✅ Paper Generated Successfully!")
            
            paper_content = f"**MITRADNYA PUBLICATIONS**\n\n"
            paper_content += f"**Subject:** {selected_subject} | **Chapters:** {', '.join(selected_chapters)}\n\n"
            paper_content += "---\n\n"
            
            st.markdown(f"<h3 style='text-align: center;'>MITRADNYA PUBLICATIONS</h3>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='text-align: center;'>Subject: {selected_subject}</h5>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'><b>Chapters:</b> {', '.join(selected_chapters)}</p>", unsafe_allow_html=True)
            st.write("---")
            
            with st.container(border=True):
                # Section A: MCQs
                if not final_mcqs.empty:
                    st.markdown("#### Q.1 Choose the correct alternative and rewrite the sentence:")
                    paper_content += "Q.1 Choose the correct alternative and rewrite the sentence:\n\n"
                    
                    for idx, row in final_mcqs.iterrows():
                        q_text = f"**{idx+1}.** {row['Question']}"
                        opts = f"A) {row['Option A']} &nbsp;&nbsp; B) {row['Option B']} &nbsp;&nbsp; C) {row['Option C']} &nbsp;&nbsp; D) {row['Option D']}"
                        
                        st.markdown(q_text)
                        st.markdown(opts, unsafe_allow_html=True)
                        st.write("")
                        
                        paper_content += f"{idx+1}. {row['Question']}\n"
                        paper_content += f"A) {row['Option A']}   B) {row['Option B']}   C) {row['Option C']}   D) {row['Option D']}\n\n"
                
                # Section B: Theory / Practical
                if not final_theory.empty:
                    st.markdown("#### Q.2 Solve the following questions:")
                    paper_content += "Q.2 Solve the following questions:\n\n"
                    
                    for idx, row in final_theory.iterrows():
                        q_text = f"**{idx+1}.** {row['Question_Text']}"
                        st.markdown(q_text)
                        st.write("")
                        
                        paper_content += f"{idx+1}. {row['Question_Text']}\n\n"
            
            st.write("---")
            # पेपर डाउनलोड करण्याचे बटन
            st.download_button(
                label="📥 Download Paper as Text File",
                data=paper_content,
                file_name=f"{selected_subject}_Test_Paper.txt",
                mime="text/plain",
                type="primary"
            )
            st.info("💡 Tip: You can press 'Ctrl + P' (or Cmd + P) on your keyboard to directly print this page or save it as a PDF!")
