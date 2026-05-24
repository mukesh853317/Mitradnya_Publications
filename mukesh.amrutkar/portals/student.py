import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# 🔴 हे नवीन लिंक ॲड करा (utils फोल्डरमधून quiz_manager फाईल आणण्यासाठी)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from utils import quiz_manager
except ImportError:
    pass # जर utils फोल्डर किंवा फाईल नसेल तर एरर येऊ नये म्हणून

# १. तुमची डिझाईन फाईल इथे इम्पोर्ट करा (तुम्ही बनवलेली design_utils.py फाईल त्याच फोल्डरमध्ये असावी)
try:
    import design_utils
except ImportError:
    pass # जर फाईल नसेल तर एरर येऊ नये म्हणून

def show_student_dashboard():
    # २. डिझाईन लागू करा (फंक्शन उपलब्ध असल्यास)
    if 'design_utils' in globals() and hasattr(design_utils, 'apply_premium_design'):
        design_utils.apply_premium_design()

    st.subheader("🎓 Student's Dashboard - Mitradnya Publication")
    
    # 🔴 सर्वात आधी API Key इथे एकदाच सेट करा (लूपच्या बाहेर)
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    except Exception:
        st.error("⚠️ Streamlit Secrets मध्ये GOOGLE_API_KEY सापडली नाही! कृपया सेटिंग्ज तपासा.")
        return # जर की नसेल तर ॲप इथेच थांबेल आणि पुढचे एरर देणार नाही

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')

    if not os.path.exists(csv_path):
        st.error("⚠️ QnA.csv File Not Found!")
        return

    # १. डेटा लोड आणि ग्रुपिंग
    df = pd.read_csv(csv_path)
    
    # ffill च्या आधी प्रश्न वेगळे करणे
    df['is_main_question'] = df['Chapter_Name'].notna() & (df['Chapter_Name'].astype(str).str.strip() != '')
    df['Question_ID'] = df['is_main_question'].cumsum()

    df['Chapter_Name'] = df['Chapter_Name'].ffill()
    df['Category'] = df['Category'].ffill()

    categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
    tab_names = ["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical", "🎯 Objective Test"]
    
    tabs = st.tabs(tab_names)

    # 🔴 पहिले ३ टॅब जुन्या पद्धतीने लोड करा (For Loop मध्ये)
    for i in range(3):
        with tabs[i]:
            cat_name = categories[i]
            cat_df = df[df['Category'].astype(str).str.strip() == cat_name]
            
            if cat_df.empty:
                st.warning("⏳ Questions for this section will be updated soon! (Stay Tuned)")
                continue
                
            grouped = cat_df.groupby('Question_ID')
            
            for q_idx, (q_id, group) in enumerate(grouped):
                first_row = group.iloc[0]
                main_title = str(first_row.get('Question_Text', ''))
                display_title = main_title[:80] + "..." if len(main_title) > 80 else main_title
                
                with st.expander(f" Q. {q_idx + 1}: {display_title}"):
                    table_data = []
                    answer_text = ""
                    
                    # AI ला देण्यासाठी संपूर्ण प्रश्न
                    q_text = "\n".join([str(row.get('Question_Text', '')).strip() for _, row in group.iterrows()])
                    
                    for _, row in group.iterrows():
                        line = str(row.get('Question_Text', '')).strip()
                        ans = str(row.get('Answer_or_Hint', '')).strip()
                        
                        if ans and ans != "nan" and ans != "Update Soon!!!":
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
                                            html_table += f"<th style='border: 1px solid #ddd; padding: 8px; text-align: center; '>{col}</th>"
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
                                    html_table += f"<th style='border: 1px solid #ddd; padding: 8px; text-align: center; '>{col}</th>"
                                else:
                                    html_table += f"<td style='border: 1px solid #ddd; padding: 8px;'>{col}</td>"
                            html_table += "</tr>"
                        html_table += "</table>"
                        st.markdown(html_table, unsafe_allow_html=True)
                    
                    # 🔴 FIX 4: बटणाच्या वरचा स्पेस कमी करण्यासाठी HTML ची छोटी रेष वापरली आहे
                    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                    
                    # AI जनरेट सोल्युशन स्ट्रीमिंगसह (Typewriter Effect)
                    if st.button("🧠 Generate Solution", key=f"btn_{cat_name}_{q_idx}", type="primary"):
                        if answer_text:
                            st.info(f"💡 **Hint:** {answer_text}")
                            
                        with st.spinner("⏳ Generating Solutions..."):
                            try:
                                model = genai.GenerativeModel('gemini-3.5-flash') 
                                
                                response = model.generate_content(
                                    f"Solve this accountancy problem in detail step-by-step:\n\n{q_text}", 
                                    stream=True,
                                    request_options={"timeout": 600}
                                )
                                                                                     
                                st.markdown("### 📝 Generated Solution:")
                                res_box = st.empty()
                                full_text = ""
                                
                                for chunk in response:
                                    full_text += chunk.text
                                    res_box.markdown(full_text + " ▌")
                                
                                res_box.markdown(full_text)
                            except Exception as e:
                                st.error(f"AI Error: {e}")

    # 🔴 ४था टॅब इथे लोड करा (लूपच्या बाहेर)
    with tabs[3]:
        st.write("---")
        # इथे आपण सर्व चॅप्टर्सचे नाव दाखवण्यासाठी ड्रॉपडाऊन (Selectbox) दिला आहे
        # किंवा तुम्ही डायरेक्ट "Chapter 1" असेही देऊ शकता
        if 'quiz_manager' in globals() and hasattr(quiz_manager, 'load_objective_test'):
            # तुमच्या Objectives.csv मधील 'No' कॉलममधील युनिक चॅप्टर्सची नावे मिळवण्यासाठी:
            obj_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Objectives.csv')
            if os.path.exists(obj_csv_path):
                obj_df = pd.read_csv(obj_csv_path)
                # 'No' कॉलममध्ये जे चॅप्टर्सचे नाव आहेत, ते ड्रॉपडाऊनमध्ये दाखवा
                chapter_list = obj_df['No'].astype(str).unique().tolist()
                
                selected_chap = st.selectbox("📝 Select Chapter for Test:", chapter_list)
                st.write("---")
                
                # निवडलेल्या चॅप्टरनुसार टेस्ट लोड करा
                quiz_manager.load_objective_test(selected_chap)
            else:
                st.warning("⚠️ Objectives.csv File Not Found in data folder!")
        else:
             st.error("⚠️ quiz_manager.py file not found in utils folder.")
