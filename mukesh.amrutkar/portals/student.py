import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal")
    
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        qna_df = pd.read_csv(csv_path)
        
        # तुमच्या हेडर्समधील स्पेलिंग जुळवून घेणे
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tab1, tab2, tab3 = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        tabs = [tab1, tab2, tab3]
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_name = categories[i]
                # 'Category' कॉलम फिल्टर करणे
                cat_df = qna_df[qna_df['Category'].astype(str).str.strip() == cat_name]
                
                if not cat_df.empty:
                    # आता आपण इंडेक्स वापरून लूप फिरवूया (ID ची गरज नाही)
                    for idx, row in cat_df.iterrows():
                        q_text = str(row['Question_Text'])
                        
                        # एक्सपँडरमध्ये प्रश्न दाखवणे
                        with st.expander(f"प्रश्न {idx + 1}: {q_text[:40]}..."):
                            st.write(q_text)
                            
                            # हिंट किंवा उत्तर दाखवणे
                            if st.button(f"💡 पहा Hint/Answer", key=f"btn_{idx}"):
                                st.success(f"उत्तर/हिंट: {row['Answer_or_Hint']}")
                else:
                    st.write("या विभागात कोणतेही प्रश्न उपलब्ध नाहीत.")
    else:
        st.error("QnA.csv फाईल सापडली नाही!")
