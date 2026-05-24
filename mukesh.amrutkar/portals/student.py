import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal 🎓")
    
    # फाईलचा पाथ
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        qna_df = pd.read_csv(csv_path)
        
        # टॅब्स बनवणे
        tab1, tab2, tab3 = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tabs = [tab1, tab2, tab3]
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_name = categories[i]
                cat_df = qna_df[qna_df['Category'].astype(str).str.strip() == cat_name]
                
                if not cat_df.empty:
                    # प्रश्न 'Question_ID' नुसार ग्रुप करणे
                    grouped = cat_df.groupby('Question_ID')
                    for q_id, group in grouped:
                        # प्रश्नाचा मजकूर एकत्र करणे
                        q_text = "\n".join([str(row.get('Question_Text', '')).strip() for _, row in group.iterrows()])
                        
                        # एक्सपँडर वापरून प्रश्न दाखवणे
                        with st.expander(f"Q. ID {q_id}: {group.iloc[0]['Question_Text'][:50]}..."):
                            st.write(q_text)
                            
                            # एआय सोल्युशन बटण (हे आपण नंतर ॲक्टिव्हेट करू शकतो)
                            if st.button(f"🧠 Solve Q-{q_id}", key=f"btn_{cat_name}_{q_id}"):
                                st.info("AI सोल्युशन प्रोसेस होत आहे...")
                else:
                    st.write("या विभागात कोणतेही प्रश्न उपलब्ध नाहीत.")
    else:
        st.error("QnA.csv फाईल सापडली नाही!")
