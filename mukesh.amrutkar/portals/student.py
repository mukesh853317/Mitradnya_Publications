import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        # १. डेटा वाचणे
        df = pd.read_csv(csv_path)
        
        # २. डेटा क्लीनिंग: रिकाम्या ओळी भरून काढणे (Forward Fill)
        df['Chapter_Name'] = df['Chapter_Name'].ffill()
        df['Category'] = df['Category'].ffill()
        
        # ३. नवीन प्रश्न ओळखण्यासाठी ग्रुपिंग (जिथे Chapter_Name बदलतो, तो नवीन प्रश्न)
        df['Question_ID'] = (df['Chapter_Name'].notna() & df['Category'].notna()).cumsum()
        
        # ४. टॅब्स तयार करणे
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        
        for i, tab in enumerate(tabs):
            with tab:
                # संबंधित कॅटेगरी फिल्टर करणे
                cat_df = df[df['Category'].str.strip() == categories[i]]
                
                # ग्रुपिंग करून प्रश्न तयार करणे
                grouped = cat_df.groupby('Question_ID')
                
                # टेबल फॉरमॅटमध्ये दाखवण्यासाठी डेटा तयार करणे
                display_data = []
                for q_id, group in grouped:
                    full_text = " ".join(group['Question_Text'].astype(str).tolist())
                    display_data.append({"Q. No.": q_id, "Question Text": full_text[:100] + "...", "Full_Text": full_text})
                
                # टेबल दाखवणे
                if display_data:
                    q_table = pd.DataFrame(display_data)
                    st.table(q_table[["Q. No.", "Question Text"]])
                    
                    # खाली सविस्तर प्रश्न आणि उत्तर पाहण्याची सोय
                    for item in display_data:
                        with st.expander(f"Q. {item['Q. No.']} See Full"):
                            st.write(item['Full_Text'])
                            if st.button(f"🔍 See Ans / Hint "):
                                st.success("Answers Will Update Here...")
                else:
                    st.write("Questions Will Update Soon!!!")
    else:
        st.error("QnA.csv File Not Found!!!")
