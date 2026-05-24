import streamlit as st
import pandas as pd
import os
import google.generativeai as genai # AI साठी हे import आवश्यक आहे

def show_student_dashboard():
    st.subheader("🎓 Mitradnya's Student Dashboard - Q&A Portal 🎓")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')

    if not os.path.exists(csv_path):
        st.error("⚠️ QnA.csv File Not Found!")
        return

    # १. डेटा लोड आणि क्लीनिंग
    df = pd.read_csv(csv_path)
    
    df['is_main_question'] = df['Chapter_Name'].notna() & (df['Chapter_Name'].astype(str).str.strip() != '')
    df['Question_ID'] = df['is_main_question'].cumsum()

    df['Chapter_Name'] = df['Chapter_Name'].ffill()
    df['Category'] = df['Category'].ffill()

    categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
    tab_names = ["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"]
    
    tabs = st.tabs(tab_names)

    for i, tab in enumerate(tabs):
        with tab:
            cat_name = categories[i] # बटणच्या key साठी cat_name
            cat_df = df[df['Category'].astype(str).str.strip() == cat_name]
            
            if cat_df.empty:
                st.warning("⏳ Questions for this section will be updated soon! (Stay Tuned)")
                continue
            
            st.write("---")
            grouped = cat_df.groupby('Question_ID')
            
            for q_idx, (q_id, group) in enumerate(grouped):
                first_row = group.iloc[0]
                main_title = str(first_row.get('Question_Text', ''))
                display_title = main_title[:80] + "..." if len(main_title) > 80 else main_title
                
                with st.expander(f" Q. {q_idx + 1}: {display_title}"):
                    table_data = []
                    answer_text = ""
                    
                    # 🤖 AI ला देण्यासाठी संपूर्ण प्रश्न एका स्ट्रिंगमध्ये तयार करणे
                    q_text = "\n".join([str(row.get('Question_Text', '')).strip() for _, row in group.iterrows()])
                    
                    for _, row in group.iterrows():
                        line = str(row.get('Question_Text', '')).strip()
                        ans = str(row.get('Answer_or_Hint', '')).strip()
                        
                        if ans and ans != "nan" and ans != "No Information":
                            answer_text = ans
                        
                        if '|' in line:
                            table_data.append([col.strip() for col in line.split('|')])
                        else:
                            if table_data:
                                html_table = "<table style='width:100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom:10px;'>"
                                for r_idx, t_row in enumerate(table_data):
                                    html_table += "<tr>"
                                    for col in t_row:
                                        if r_idx == 0:
                                            html_table += f"<th style='border: 1px solid #ddd; padding: 8px; text-align: center;'>{col}</th>"
                                        else:
                                            html_table += f"<td style='border: 1px solid #ddd; padding: 8px;'>{col}</td>"
                                    html_table += "</tr>"
                                html_table += "</table>"
                                st.markdown(html_table, unsafe_allow_html=True)
                                table_data = []
                            
                            if line:
                                st.markdown(line)
                    
                    if table_data:
                        html_table = "<table style='width:100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom:10px;'>"
                        for r_idx, t_row in enumerate(table_data):
                            html_table += "<tr>"
                            for col in t_row:
                                if r_idx == 0:
                                    html_table += f"<th style='border: 1px solid #ddd; padding: 8px; text-align: center;'>{col}</th>"
                                else:
                                    html_table += f"<td style='border: 1px solid #ddd; padding: 8px;'>{col}</td>"
                            html_table += "</tr>"
                        html_table += "</table>"
                        st.markdown(html_table, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # 🎯 तुम्ही दिलेला AI जनरेट सोल्युशनचा कोड
                    if st.button("🧠 Generate Solution", key=f"btn_{cat_name}_{q_idx}"):
                        with st.spinner("⏳ Generating Solution..."):
                            try:
                                # Tumcha model tasach theva kiva 'gemini-1.5-flash' try kara
                                model = genai.GenerativeModel('gemini-3.5-flash') 
                                
                                # stream=True add kela ahe, yamule answer lagach disel
                                response = model.generate_content(f"Solve this accountancy problem in detail:\n\n{q_text}", stream=True)
            
                                st.markdown("### 📝 AI Generated Solution:")
            
                                # Text type vhayla survat honyasathi placeholder
                                res_box = st.empty()
                                full_text = ""
            
                                # Loop madhye answer thode thode add hoil (Streaming Effect)    
                                for chunk in response:
                                    full_text += chunk.text
                                    res_box.markdown(full_text + " ▌") # ▌ ha cursor sarkha disel
            
                                # Purna generate jhalyavar cursor kadhun takaycha
                                res_box.markdown(full_text)
            
                        except Exception as e:
                            st.error(f"AI Error: {e}")
