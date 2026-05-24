import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')

    if not os.path.exists(csv_path):
        st.error("⚠️ QnA.csv File Not Found!")
        return

    # १. डेटा लोड करणे
    df = pd.read_csv(csv_path)
    
    # २. डेटा क्लीनिंग
    df['Chapter_Name'] = df['Chapter_Name'].ffill()
    df['Category'] = df['Category'].ffill()
    
    # ३. नवीन प्रश्न ओळखण्यासाठी ग्रुपिंग (Question_ID तयार करणे)
    df['is_main_question'] = df['Chapter_Name'].notna() & df['Category'].notna()
    df['Question_ID'] = df['is_main_question'].cumsum()

    categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
    tab_names = ["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"]
    
    # टॅब्स तयार करणे
    tabs = st.tabs(tab_names)

    for i, tab in enumerate(tabs):
        with tab:
            # त्या-त्या टॅबचा डेटा फिल्टर करणे
            cat_df = df[df['Category'].astype(str).str.strip() == categories[i]]
            
            if cat_df.empty:
                st.warning("⏳ Questions for this section will be updated soon! (Stay Tuned)")
                continue
            
            st.write("---")
            grouped = cat_df.groupby('Question_ID')
            
            for q_idx, (q_id, group) in enumerate(grouped):
                # मुख्य प्रश्न (Title) मिळवणे
                first_row = group.iloc[0]
                main_title = str(first_row.get('Question_Text', ''))
                display_title = main_title[:80] + "..." if len(main_title) > 80 else main_title
                
                # एक्सपँडर (Expander)
                with st.expander(f"Q. {q_idx + 1}: {display_title}"):
                    table_data = []
                    answer_text = ""
                    
                    for _, row in group.iterrows():
                        line = str(row.get('Question_Text', '')).strip()
                        ans = str(row.get('Answer_or_Hint', '')).strip()
                        
                        if ans and ans != "nan" and ans != "माहिती उपलब्ध नाही":
                            answer_text = ans
                        
                        # जर ओळीत '|' असेल, तर ते टेबलमध्ये टाका
                        if '|' in line:
                            table_data.append([col.strip() for col in line.split('|')])
                        else:
                            # जर जुना टेबल डेटा शिल्लक असेल, तर तो HTML टेबल म्हणून रेंडर करा
                            if table_data:
                                html_table = "<table style='width:100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom:10px;'>"
                                for r_idx, t_row in enumerate(table_data):
                                    html_table += "<tr>"
                                    for col in t_row:
                                        if r_idx == 0: # हेडर
                                            html_table += f"<th style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2; text-align: center;'>{col}</th>"
                                        else: # डेटा
                                            html_table += f"<td style='border: 1px solid #ddd; padding: 8px;'>{col}</td>"
                                    html_table += "</tr>"
                                html_table += "</table>"
                                st.markdown(html_table, unsafe_allow_html=True)
                                table_data = [] # टेबल प्रिंट झाल्यावर रिकामा करा
                            
                            # जर साधा मजकूर असेल, तर तो प्रिंट करा
                            if line:
                                st.markdown(line)
                    
                    # लूप संपल्यावर जर काही टेबल डेटा उरला असेल, तर तो प्रिंट करा
                    if table_data:
                        html_table = "<table style='width:100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom:10px;'>"
                        for r_idx, t_row in enumerate(table_data):
                            html_table += "<tr>"
                            for col in t_row:
                                if r_idx == 0:
                                    html_table += f"<th style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2; text-align: center;'>{col}</th>"
                                else:
                                    html_table += f"<td style='border: 1px solid #ddd; padding: 8px;'>{col}</td>"
                            html_table += "</tr>"
                        html_table += "</table>"
                        st.markdown(html_table, unsafe_allow_html=True)
                    
                    # 🎯 नेहमी दिसणारे Generate Solution बटन
                    st.markdown("---")
                    # बटण की (Key) युनिक करण्यासाठी 'categories[i]' चा वापर
                    if st.button(f"🧠 Generate Solution", key=f"btn_gen_{categories[i]}_{q_idx}"):
                        if answer_text:
                            st.success("✅ Solution Generated Successfully!")
                            st.markdown(f"**Answer / Hint:** \n{answer_text}")
                        else:
                            st.info("💡 Detailed solution for this question will be updated soon!")
