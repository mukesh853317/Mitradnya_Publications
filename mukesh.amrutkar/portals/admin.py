import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# Function to clean question text (Removes "Q81:", "Q113:" etc.)
def clean_question(text):
    import re
    # 'Q' नंतर येणारे अंक आणि ':' काढून टाकेल
    return re.sub(r'Q\d+[:.]\s*', '', str(text))

def show_admin_panel():
    st.markdown("<h2 style='color: #1e3a8a;'>Board Paper Generator</h2>", unsafe_allow_html=True)
    
    qna_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    if not os.path.exists(qna_path):
        st.error("Data file missing!")
        return
    df = pd.read_csv(qna_path).astype(str)
    
    sub = st.selectbox("Select Subject:", df['Subject'].unique())
    chaps = st.multiselect("Select Chapters:", df[df['Subject'] == sub]['Chapter_Name'].unique())
    
    if st.button("🚀 Generate Clean Professional Paper"):
        paper = df[(df['Subject'] == sub) & (df['Chapter_Name'].isin(chaps))]
        
        if not paper.empty:
            tab1, tab2 = st.tabs(["📄 Board Paper", "✅ AI Solution"])
            
            with tab1:
                st.markdown("### 📄 Professional Paper")
                for i, row in paper.iterrows():
                    # इथे आपण क्लीन केलेला प्रश्न दाखवतोय
                    clean_q = clean_question(row['Question_Text'])
                    st.markdown(f"**Q.{i+1}.** {clean_q}")
                    st.write("---")
            
            with tab2:
                st.markdown("### Generate Solutions")
                if st.button("Generate Solution for Paper"):
                    with st.spinner("Generating..."):
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content(f"Solve these accounting problems: {paper['Question_Text'].to_list()}")
                        st.markdown(res.text)
        else:
            st.warning("No questions found!")

show_admin_panel()
