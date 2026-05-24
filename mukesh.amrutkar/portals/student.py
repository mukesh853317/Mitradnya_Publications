import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        # १. डेटा वाचणे
        df = pd.read_csv(csv_path)
        
        # २. डेटा क्लीनिंग
        df['Chapter_Name'] = df['Chapter_Name'].ffill()
        df['Category'] = df['Category'].ffill()
        
        # ३. नवीन प्रश्न ओळखण्यासाठी ग्रुपिंग
        df['Question_ID'] = (df['Chapter_Name'].notna() & df['Category'].notna()).cumsum()
        
        # ४. टॅब्स तयार करणे
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
        
        for i, tab in enumerate(tabs):
            with tab:
                # कॅटेगरी फिल्टर करणे
                cat_df = df[df['Category'].str.strip() == categories[i]]
                
                if cat_df.empty:
                    st.write("Questions will update soon!!!")
                    continue
                
                # प्रश्न ग्रुपिंग
                grouped = cat_df.groupby('Question_ID')
                
                # टेबल दाखवण्यासाठी आणि बटण की (Key) मॅनेज करण्यासाठी लूप
                q_list = []
                for q_id, group in grouped:
                    full_text = " ".join(group['Question_Text'].astype(str).tolist())
                    q_list.append({"ID": q_id, "Text": full_text})
                
                # टेबल दाखवणे
                table_df = pd.DataFrame([{"Q. No.": item["ID"], "Question Text": item["Text"][:100] + "..."} for item in q_list])
                st.table(table_df)
                
                # खाली सविस्तर प्रश्न आणि उत्तर पाहण्याची सोय (युनिक की सह)
                for item in q_list:
                    with st.expander(f"Q. {item['ID']} See Full"):
                        st.write(item['Text'])
                        
                        # इथे युनिक 'key' दिली आहे जेणेकरून एरर येणार नाही
                        if st.button(f"🔍 See Ans / Hint for Q.{item['ID']}", key=f"ans_{categories[i]}_{item['ID']}"):
                            st.success("Answers Will Update Here...")
    else:
        st.error("QnA.csv File Not Found!!!")
