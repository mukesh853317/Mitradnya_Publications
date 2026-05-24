import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # डेटा क्लीनिंग
        df['Chapter_Name'] = df['Chapter_Name'].ffill()
        df['Category'] = df['Category'].ffill()
        
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_df = df[df['Category'].str.strip() == categories[i]]
                
                # प्रश्न ग्रुपिंग (QnA.csv नुसार)
                grouped = cat_df.groupby('Question_Text')
                
                for q_text, group in grouped:
                    # प्रश्न जसा आहे तसा दाखवणे
                    with st.expander(f"प्रश्न: {str(q_text)[:60]}..."):
                        st.write(q_text)
                        
                        # उत्तर/हिंट विभाग
                        answer = group['Answer_or_Hint'].iloc[0]
                        if not pd.isna(answer):
                            if st.button(f"🔍 Show Answer / Hint", key=f"btn_{q_text}"):
                                st.success(str(answer))
    else:
        st.error("Data File Not Found!")
