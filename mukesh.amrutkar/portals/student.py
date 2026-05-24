import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # डेटा क्लीनिंग (रिकाम्या ओळी भरून काढणे)
        df['Chapter_Name'] = df['Chapter_Name'].ffill()
        df['Category'] = df['Category'].ffill()
        
        # नवीन प्रश्न ओळखणे (Chapter किंवा Category बदलली की नवीन प्रश्न)
        df['Question_ID'] = (df['Chapter_Name'].notna() & df['Category'].notna()).cumsum()
        
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_df = df[df['Category'].str.strip() == categories[i]]
                grouped = cat_df.groupby('Question_ID')
                
                for q_id, group in grouped:
                    # प्रश्न मजकूर (नंबर न देता)
                    full_q_text = group['Question_Text'].iloc[0]
                    st.markdown(f"**{full_q_text}**")
                    
                    # ट्रायल बॅलन्स टेबल तयार करणे
                    tb_data = []
                    for _, row in group.iloc[1:].iterrows():
                        text = str(row['Question_Text'])
                        if '|' in text:
                            # पाइप (|) चिन्हाने तुकडे करून टेबलमध्ये टाकणे
                            parts = [p.strip() for p in text.split('|')]
                            tb_data.append(parts)
                    
                    if tb_data:
                        # टेबलचे कॉलम्स
                        tb_df = pd.DataFrame(tb_data, columns=["Particulars", "Debit ₹", "Credit ₹"])
                        st.table(tb_df)
                    
                    # उत्तर/हिंट बटण
                    if st.button(f"🔍 Show Answer / Hint", key=f"btn_{q_id}"):
                        st.success(f"**Solution:** {group['Answer_or_Hint'].iloc[0]}")
                    
                    st.divider() # दोन प्रश्नांमध्ये रेषा
    else:
        st.error("QnA.csv File Not Found!")
