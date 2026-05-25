import streamlit as st
import pandas as pd
import os

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>👨‍🏫 Admin Portal - Paper Generator</h2>", unsafe_allow_html=True)
    
    # 1. डेटा लोड करा
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("⚠️ QnA.csv फाईल सापडली नाही!")
        return
    qna_df = pd.read_csv(qna_path).astype(str).apply(lambda x: x.str.strip())
    
    all_subjects = qna_df['Subject'].unique().tolist()
    
    # 2. सिलेक्शन (Selection)
    col1, col2 = st.columns(2)
    with col1:
        selected_sub = st.selectbox("🎯 विषय निवडा:", all_subjects)
    
    all_chaps = sorted(qna_df[qna_df['Subject'] == selected_sub]['Chapter_Name'].unique().tolist())
    with col2:
        selected_chaps = st.multiselect("📑 धडे निवडा:", all_chaps, default=all_chaps[:1])
        
    # 3. प्रश्न प्रकार निवडा
    st.markdown("##### 🎯 प्रश्नांचे प्रकार निवडा:")
    c1, c2, c3 = st.columns(3)
    with c1: use_prac = st.checkbox("Practical Problems", value=True)
    with c2: use_short = st.checkbox("Short Notes", value=True)
    with c3: use_theory = st.checkbox("Theory Questions", value=True)
    
    if st.button("🚀 पेपर आणि उत्तरे जनरेट करा"):
        cats = []
        if use_prac: cats.append('Exercise_Problems')
        if use_short: cats.append('Short_Notes')
        if use_theory: cats.append('One_Sentence')
        
        # डेटा फिल्टर करा
        paper = qna_df[(qna_df['Subject'] == selected_sub) & 
                       (qna_df['Chapter_Name'].isin(selected_chaps)) & 
                       (qna_df['Category'].isin(cats))]
        
        if paper.empty:
            st.warning("⚠️ या निवडीसाठी प्रश्न सापडले नाहीत!")
        else:
            st.success(f"✅ एकूण {len(paper)} प्रश्न जनरेट झाले आहेत.")
            
            # टॅब्स बनवा
            tab1, tab2 = st.tabs(["📄 Question Paper", "✅ Answer Key"])
            
            with tab1:
                st.markdown("### 📄 Question Paper")
                for i, row in paper.iterrows():
                    st.write(f"**Q{i+1}:** {row['Question_Text']}")
            
            with tab2:
                st.markdown("### ✅ Answer Key")
                for i, row in paper.iterrows():
                    # इथे 'Answer' कॉलम चेक केला जातो
                    ans = row.get('Answer', 'N/A')
                    st.write(f"**Ans {i+1}:** {ans}")
                
            # डाउनलोड बटन (एकत्रित)
            full_content = "--- QUESTION PAPER ---\n\n"
            for i, row in paper.iterrows(): full_content += f"Q{i+1}: {row['Question_Text']}\n\n"
            
            full_content += "\n--- ANSWER KEY ---\n\n"
            for i, row in paper.iterrows(): full_content += f"Ans {i+1}: {row.get('Answer', 'N/A')}\n\n"
            
            st.download_button("📥 पेपर आणि उत्तरे डाऊनलोड करा", data=full_content, file_name="Paper_With_Answers.txt")

# फंक्शन कॉल
show_admin_panel()
