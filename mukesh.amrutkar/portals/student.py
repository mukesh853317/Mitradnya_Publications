import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        qna_df = pd.read_csv(csv_path)
        
        # 'Category' फिल्टर करणे
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_df = qna_df[qna_df['Category'].astype(str).str.strip() == categories[i]]
                
                for idx, row in cat_df.iterrows():
                    # पूर्ण प्रश्न दाखवण्यासाठी :40 काढले आहे
                    q_text = str(row['Question_Text'])
                    
                    with st.expander(f"Q. {q_text[:60]}..."): # हेडरमध्ये फक्त थोडी हिंट दिसेल
                        st.write("### Full Question")
                        st.info(q_text) # पूर्ण प्रश्न इथे वाचता येईल
                        
                        # डिटेल उत्तरासाठी स्वतंत्र विभाग
                        with st.expander("📝 Show Ans / Hint "):
                            st.success(f"{row['Answer_or_Hint']}")
                            
                            # AI सोल्युशनसाठी बटण
                            if st.button(f"🧠 Generate Answer", key=f"ai_{idx}"):
                                st.write("Generating Answer...")
    else:
        st.error("No Data File!")
