import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# AI Configuration
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    pass

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>👨‍🏫 Admin Portal - Automatic Solution Generator</h2>", unsafe_allow_html=True)
    
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("⚠️ QnA.csv File not Found!")
        return
    qna_df = pd.read_csv(qna_path).astype(str).apply(lambda x: x.str.strip())
    
    all_subjects = qna_df['Subject'].unique().tolist()
    selected_sub = st.selectbox("🎯 Select Subject:", all_subjects)
    
    # चेकबॉक्सेस
    st.markdown("##### 🎯 Select Questions:")
    c1, c2, c3 = st.columns(3)
    with c1: use_prac = st.checkbox("Practical", value=True)
    with c2: use_short = st.checkbox("Short Notes", value=True)
    with c3: use_theory = st.checkbox("Theory", value=True)
    
    if st.button("🚀 Generate Paper & Solution"):
        cats = []
        if use_prac: cats.append('Exercise_Problems')
        if use_short: cats.append('Short_Notes')
        if use_theory: cats.append('One_Sentence')
        
        paper = qna_df[(qna_df['Subject'] == selected_sub) & (qna_df['Category'].isin(cats))]
        
        if not paper.empty:
            st.success("✅ Paper is Ready!")
            
            for i, row in paper.iterrows():
                st.write(f"**Q{i+1}:** {row['Question_Text']}")
                
                # 🔴 AUTOMATIC ANSWER GENERATOR
                if row.get('Answer') == 'nan' or not row.get('Answer'):
                    if st.button(f"Generate Answer for Q{i+1}", key=f"ai_{i}"):
                        with st.spinner("Generating Answer..."):
                            model = genai.GenerativeModel('gemini-3.5-flash')
                            response = model.generate_content(f"Answer this question shortly: {row['Question_Text']}")
                            st.info(f"Ans: {response.text}")
                else:
                    st.write(f"**Ans:** {row['Answer']}")
        else:
            st.warning("⚠️ प्रश्न सापडले नाहीत!")

show_admin_panel()
