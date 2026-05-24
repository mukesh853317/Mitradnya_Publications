import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # १. डेटा क्लीन करणे
        df['Chapter_Name'] = df['Chapter_Name'].ffill()
        df['Category'] = df['Category'].ffill()
        
        # २. प्रश्न ग्रुप करणे
        df['Question_ID'] = (df['Chapter_Name'].notna() & df['Category'].notna()).cumsum()
        
        # ३. टॅब्स तयार करणे
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_df = df[df['Category'].str.strip() == categories[i]]
                grouped = cat_df.groupby('Question_ID')
                
                for q_id, group in grouped:
                    # प्रश्न आणि ट्रायल बॅलन्स टेबल तयार करणे
                    full_q_text = group['Question_Text'].iloc[0]
                    st.markdown(f"### Q.{q_id}: {full_q_text}")
                    
                    # ट्रायल बॅलन्स टेबल फॉरमॅटमध्ये बदलणे
                    tb_data = []
                    for _, row in group.iloc[1:].iterrows():
                        text = str(row['Question_Text'])
                        if '|' in text:
                            parts = text.split('|')
                            tb_data.append([p.strip() for p in parts])
                    
                    if tb_data:
                        tb_df = pd.DataFrame(tb_data)
                        st.table(tb_df) # टेबल फॉरमॅट
                    
                    # उत्तर/हिंट बटण
                    if st.button(f"🔍 See Ans / Hint for Q.{q_id}", key=f"btn_{q_id}"):
                        st.success("Detailed solution will be displayed here...")
    else:
        st.error("Data File Not Found!")
