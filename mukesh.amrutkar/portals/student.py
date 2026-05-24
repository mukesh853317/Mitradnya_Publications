import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard 🎓")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        qna_df = pd.read_csv(csv_path)
        
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        
        for i, tab in enumerate(tabs):
            with tab:
                # डेटा फिल्टर करणे
                cat_df = qna_df[qna_df['Category'].astype(str).str.strip() == categories[i]]
                
                if cat_df.empty:
                    st.write("Will Update Questions Soon!!!")
                    continue
                
                for idx, row in cat_df.iterrows():
                    q_text = str(row['Question_Text'])
                    
                    # एक्सपँडरचे नाव (Q. नंबर दिसेल)
                    with st.expander(f"Q. {idx + 1}: {q_text}..."):
                        
                        # पूर्ण प्रश्न दिसण्यासाठी text_area वापरले आहे
                        st.text_area("Full Question:", value=q_text, height=150, key=f"q_text_{idx}")
                        
                        # उत्तराचा विभाग
                        with st.expander("📝 Show Ans / Hint"):
                            st.success(str(row['Answer_or_Hint']))
                            
                            # AI जनरेट बटण
                            if st.button(f"🧠 Generate Answer", key=f"ai_{idx}"):
                                with st.spinner("Generating AI Answer..."):
                                    # इथे तुमचे AI लॉजिक येईल
                                    st.write("Generating Detailed Answer...") 
    else:
        st.error("No Data File found at " + csv_path)
