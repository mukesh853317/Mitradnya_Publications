import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # डेटा क्लीनिंग (रिकाम्या ओळी काढून टाकणे)
        df = df.dropna(subset=['Question_Text'])
        
        # कॅटेगरीनुसार टॅब्स
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_df = df[df['Category'].astype(str).str.strip() == categories[i]]
                
                # प्रत्येक प्रश्नासाठी लूप
                for idx, row in cat_df.iterrows():
                    q_text = str(row['Question_Text'])
                    
                    # जर ओळीत '|' नसेल, तर तो मुख्य प्रश्न आहे
                    if '|' not in q_text:
                        with st.expander(f"प्रश्न: {q_text[:50]}..."):
                            st.markdown(f"**{q_text}**")
                            
                            # खाली उत्तर बटण
                            if st.button(f"🔍 उत्तर पहा", key=f"btn_{idx}"):
                                st.success(str(row['Answer_or_Hint']))
                    
                    # जर ओळीत '|' असेल, तर ते ट्रायल बॅलन्सचे टेबल आहे (हे टेबल फॉरमॅटमध्ये दिसेल)
                    elif '|' in q_text:
                        # हे ट्रायल बॅलन्सचे टेबल म्हणून दाखवा
                        st.text(q_text) 
    else:
        st.error("Data File Not Found!")
