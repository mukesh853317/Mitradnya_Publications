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
                cat_df = qna_df[qna_df['Category'].astype(str).str.strip() == categories[i]]
                
                if cat_df.empty:
                    st.write("Will Update Soon.")
                    continue
                
                # प्रश्न टेबल फॉरमॅटमध्ये दाखवणे
                st.write("### 📝 List of Questions:")
                for idx, row in cat_df.iterrows():
                    # फक्त प्रश्न दिसतोय
                    with st.expander(f"Q. {idx + 1}: {str(row['Question_Text'])[:50]}..."):
                        st.markdown(f"**Full Question:**\n\n{row['Question_Text']}")
                        
                        # आता खाली बटण आहे, जे दाबल्यावरच उत्तर दिसेल
                        if st.button(f"🔍 Ans / Hint (Q. {idx + 1})", key=f"ans_btn_{idx}"):
                            st.divider()
                            st.success(f"** Ans/ Hint :**\n\n{row['Answer_or_Hint']}")
                            
                            # AI सोल्युशन बटण उत्तराच्या खाली
                            if st.button(f"🧠 Generate Answer", key=f"ai_{idx}"):
                                st.info("Generating Answer...")
    else:
        st.error("No Data File found!")
