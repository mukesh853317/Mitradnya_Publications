import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import sys

# नवीन लिंक ॲड करा (utils फोल्डरमधून quiz_manager फाईल आणण्यासाठी)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from utils import quiz_manager
except ImportError:
    pass 

# १. तुमची डिझाईन फाईल इथे इम्पोर्ट करा 
try:
    import design_utils
except ImportError:
    pass 

def show_student_dashboard():
    # २. डिझाईन लागू करा 
    if 'design_utils' in globals() and hasattr(design_utils, 'apply_premium_design'):
        design_utils.apply_premium_design()

    st.subheader("🎓 Student's Dashboard - Mitradnya Publication")
    
    # API Key एकदाच सेट करा 
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    except Exception:
        st.error("⚠️ Streamlit Secrets: GOOGLE_API_KEY is missing! Please check settings.")
        return 

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')

    if not os.path.exists(csv_path):
        st.error("⚠️ QnA.csv File Not Found in data folder!")
        return

    # डेटा लोड 
    df = pd.read_csv(csv_path)
    
    # ffill च्या आधी प्रश्न वेगळे करणे
    df['is_main_question'] = df['Chapter_Name'].notna() & (df['Chapter_Name'].astype(str).str.strip() != '')
    df['Question_ID'] = df['is_main_question'].cumsum()

    # जर CSV मध्ये Subject कॉलम नसेल, तर तात्पुरता 'BK' म्हणून सेट करू
    if 'Subject' not in df.columns:
        df['Subject'] = 'BK'

    df['Subject'] = df['Subject'].ffill()
    df['Chapter_Name'] = df['Chapter_Name'].ffill()
    df['Category'] = df['Category'].ffill()

    # ==============================================================
    # २ स्तरांचे ग्लोबल फिल्टर (Subject -> Chapter)
    # ==============================================================
    st.markdown("<h4 style='color: #4b5563; margin-bottom: 5px;'>📚 Select Subject & Chapter:</h4>", unsafe_allow_html=True)
    
    col_sub, col_chap = st.columns(2)
    
    with col_sub:
        subject_list = df['Subject'].dropna().astype(str).unique().tolist()
        selected_subject = st.selectbox("Select Subject", subject_list, key="global_subject_select")
        
    df_subject = df[df['Subject'].astype(str).str.strip() == str(selected_subject).strip()]
    
    with col_chap:
        chapter_list = df_subject['Chapter_Name'].dropna().astype(str).unique().tolist()
        selected_chapter = st.selectbox("Select Chapter", chapter_list, key="global_chapter_select")
        
    df_filtered = df_subject[df_subject['Chapter_Name'].astype(str).str.strip() == str(selected_chapter).strip()]

    # मुख्य ४ टॅब्स 
    main_tab_names = [
        "📚 Study Room", 
        "📄 Board Papers & Solutions", 
        "🎯 Objective Test",
        "📈 My Progress"
    ]
    main_tabs = st.tabs(main_tab_names)

    # ==========================================
    # १. Study Room (यात पहिले ३ टॅब्स येतील)
    # ==========================================
    with main_tabs[0]:
        categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
        sub_tab_names = ["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"]
        sub_tabs = st.tabs(sub_tab_names)

        for i in range(3):
            with sub_tabs[i]:
                cat_name = categories[i]
                cat_df = df_filtered[df_filtered['Category'].astype(str).str.strip() == cat_name]
                
                if cat_df.empty:
                    st.info(f"💡 No questions found in '{sub_tab_names[i].split(' ', 1)[1]}' for {selected_chapter} yet.")
                    continue
                
                grouped = cat_df.groupby('Question_ID')
                
                for q_idx, (q_id, group) in enumerate(grouped):
                    first_row = group.iloc[0]
                    main_title = str(first_row.get('Question_Text', ''))
                    display_title = main_title[:80] + "..." if len(main_title) > 80 else main_title
                    
                    with st.expander(f" Q. {q_idx + 1}: {display_title}"):
                        table_data = []
                        answer_text = ""
                        
                        q_text = "\n".join([str(row.get('Question_Text', '')).strip() for _, row in group.iterrows()])
                        
                        for _, row in group.iterrows():
                            line = str(row.get('Question_Text', '')).strip()
                            ans = str(row.get('Answer_or_Hint', '')).strip()
                            
                            if ans and str(ans).lower() != "nan" and ans != "Update Soon!!!":
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
                        
                        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                        
                        # AI जनरेट सोल्युशन
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

    # ==========================================
    # २. Board Papers & Solutions
    # ==========================================
    with main_tabs[1]:
        st.markdown(f"<h3 style='color: #1e3a8a;'>📄 Board Question Papers ({selected_subject})</h3>", unsafe_allow_html=True)
        st.info(f"💡 Previous years' board question papers for {selected_subject} will be available here soon.")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.selectbox("🗓️ Select Exam Year / Exam Paper:", ["March 2024", "July 2023", "March 2023", "March 2022"])
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("📥 Download PDF", disabled=True) 

    # ==========================================
    # ३. Objective Test 
    # ==========================================
    with main_tabs[2]:
        if 'quiz_manager' in globals() and hasattr(quiz_manager, 'load_objective_test'):
            quiz_manager.load_objective_test(selected_subject, selected_chapter)
        else:
            st.error("⚠️ quiz_manager.py file not found in utils folder.") # 🔴 FIXED INDENTATION HERE

    # ==========================================
    # ४. My Progress 
    # ==========================================
    with main_tabs[3]:
        st.markdown(f"<h3 style='color: #1e3a8a;'>📈 Your Performance Analytics ({selected_subject})</h3>", unsafe_allow_html=True)
        
        results_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'results.csv')
        
        if os.path.exists(results_path):
            try:
                res_df = pd.read_csv(results_path)
                res_filtered = res_df[res_df['Subject'].astype(str).str.strip() == str(selected_subject).strip()]
                
                if not res_filtered.empty:
                    total_tests = len(res_filtered)
                    avg_per = res_filtered['Percentage'].mean()
                    highest_per = res_filtered['Percentage'].max()
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric(label="Total Tests Attempted", value=str(total_tests))
                    col2.metric(label="Average Percentage", value=f"{avg_per:.1f}%")
                    col3.metric(label="Highest Percentage", value=f"{highest_per:.1f}%")
                    
                    st.write("---")
                    st.markdown("#### 📊 Test Score History:")
                    
                    display_df = res_filtered[["Chapter", "Score", "Total", "Percentage", "Date"]].sort_index(ascending=False)
                    st.dataframe(display_df, use_container_width=True)
                    
                    st.write("---")
                    st.markdown("#### 📈 Progress Chart (Percentage Over Time):")
                    chart_data = res_filtered[["Date", "Percentage"]].set_index("Date")
                    st.line_chart(chart_data)
                    
                else:
                    st.info(f"💡 No tests attempted yet for {selected_subject}. Complete a test to see your analytics!")
            except Exception as e:
                st.error(f"Error loading analytics: {e}")
        else:
            st.info("⏳ No test history found. Complete your first Objective Test to unlock the progress tracker!")
