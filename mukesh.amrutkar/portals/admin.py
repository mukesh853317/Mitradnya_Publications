import streamlit as st
import pandas as pd
import os

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>👨‍🏫 Admin Portal - Advanced Paper Generator</h2>", unsafe_allow_html=True)
    st.info("💡 Select Subject, Chapters, and Question Types to generate a Custom Practice Paper.")
    
    # 1. Load Data
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("⚠️ QnA.csv file missing in 'data' folder!")
        return
    qna_df = pd.read_csv(qna_path).astype(str).apply(lambda x: x.str.strip())
    
    all_subjects = qna_df['Subject'].unique().tolist()
    
    # 2. Selection UI
    col1, col2 = st.columns(2)
    with col1:
        selected_sub = st.selectbox("🎯 Select Subject:", all_subjects)
    
    all_chaps = qna_df[qna_df['Subject'] == selected_sub]['Chapter_Name'].unique().tolist()
    with col2:
        selected_chaps = st.multiselect("📑 Select Chapters:", sorted(all_chaps), default=all_chaps[:1])
    
    # 3. Question Type Selection
    st.markdown("##### 🎯 Choose Question Types:")
    c1, c2, c3 = st.columns(3)
    with c1: use_prac = st.checkbox("Practical Problems", value=True)
    with c2: use_short = st.checkbox("Short Notes", value=True)
    with c3: use_theory = st.checkbox("Theory Questions", value=True)
    
    if st.button("🚀 Generate Custom Paper"):
        # Category Mapping
        cats = []
        if use_prac: cats.append('Exercise_Problems')
        if use_short: cats.append('Short_Notes')
        if use_theory: cats.append('One_Sentence')
        
        # Filter Logic
        paper = qna_df[(qna_df['Subject'] == selected_sub) & 
                       (qna_df['Chapter_Name'].isin(selected_chaps)) & 
                       (qna_df['Category'].isin(cats))]
        
        if paper.empty:
            st.warning("⚠️ No questions found for these selections!")
        else:
            st.success(f"✅ Generated {len(paper)} questions.")
            
            # Display Paper
            st.markdown("---")
            st.markdown("### 📄 Question Paper")
            for i, row in paper.iterrows():
                st.write(f"**Q{i+1}:** {row['Question_Text']}")
            
            # Download
            csv_data = paper[['Chapter_Name', 'Category', 'Question_Text']].to_csv(index=False)
            st.download_button("📥 Download Paper (CSV)", data=csv_data, file_name="Custom_Paper.csv")

show_admin_panel()
