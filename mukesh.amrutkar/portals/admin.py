import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from fpdf import FPDF

# AI Configuration
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    pass

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>🏛️ Mitradnya Professional Board Paper Generator</h2>", unsafe_allow_html=True)
    
    # 1. डेटा लोड करा
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("⚠️ QnA.csv फाईल सापडली नाही!")
        return
    qna_df = pd.read_csv(qna_path).astype(str).apply(lambda x: x.str.strip())
    
    all_subjects = qna_df['Subject'].unique().tolist()
    selected_sub = st.selectbox("🎯 विषय निवडा:", all_subjects)
    
    all_chaps = sorted(qna_df[qna_df['Subject'] == selected_sub]['Chapter_Name'].unique().tolist())
    selected_chaps = st.multiselect("📑 धडे निवडा:", all_chaps, default=all_chaps[:1])
    
    # चेकबॉक्सेस (प्रश्न प्रकार)
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
        
        paper = qna_df[(qna_df['Subject'] == selected_sub) & 
                       (qna_df['Chapter_Name'].isin(selected_chaps)) & 
                       (qna_df['Category'].isin(cats))]
        
        if paper.empty:
            st.warning("⚠️ या निवडीसाठी प्रश्न सापडले नाहीत!")
        else:
            # टॅब्स बनवा
            tab1, tab2 = st.tabs(["📄 Professional Question Paper", "✅ AI Generated Solutions"])
            
            with tab1:
                st.markdown("### 📄 Board Pattern Question Paper")
                for i, row in paper.iterrows():
                    st.write(f"**Q{i+1}:** {row['Question_Text']}")
                
                # PDF साठी इथे लॉजिक वाढवू शकता
                
            with tab2:
                st.markdown("### ✅ AI Generated Solutions")
                for i, row in paper.iterrows():
                    with st.expander(f"Generate Solution for Q{i+1}"):
                        if st.button(f"🤖 Get Solution for Q{i+1}", key=f"ai_{i}"):
                            with st.spinner("AI उत्तर लिहित आहे..."):
                                model = genai.GenerativeModel('gemini-1.5-flash')
                                response = model.generate_content(f"Answer the following question clearly: {row['Question_Text']}")
                                st.write(response.text)

# फंक्शन कॉल
show_admin_panel()
