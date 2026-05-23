import streamlit as st
import pandas as pd
import smtplib
import requests
import urllib.parse
from email.mime.text import MIMEText
import random
import streamlit.components.v1 as components
import re
import os
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="📚 Mitradnya Publication's Online Exam 📚", page_icon="📝", layout="centered")

# Authentication and State
if 'is_authenticated' not in st.session_state: st.session_state.is_authenticated = False
if 'test_status' not in st.session_state: st.session_state.test_status = 'not_started'

# API Key Config
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    pass

# Data Loading
@st.cache_data
def load_all_data():
    try:
        df = pd.read_csv('All in one.csv').fillna("None")
        qna_df = pd.read_csv('QnA.csv').fillna("")
        qna_df['Chapter_Name'] = qna_df['Chapter_Name'].ffill()
        qna_df['Category'] = qna_df['Category'].ffill()
        return df, qna_df
    except:
        return None, None

df, qna_df = load_all_data()

# App Layout
st.sidebar.markdown("## 📚 Mitradnya Publication's")
if df is not None:
    chapter_col = df.columns[0]
    selected_chapter = st.sidebar.selectbox("Select Chapter:", df[chapter_col].unique())
    
    st.title("📚 Mitradnya Publication's Portal")
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Exam Portal", "📖 Study Room", "📓 Q & A Bank", "📄 Papers"])
        
        with tab1:
            if selected_part != "Test 1" and not st.session_state.is_authenticated:
                st.error("🔒 Premium Test Locked")
                st.warning("⚠️ This test is for Premium Students only. 'Test 1' is available for free practice.")
                test_key = st.text_input("🔑 Enter Premium Key:", key="test_key", type="password")
                if st.button("Unlock All Tests 🚀"):
                    if test_key in VALID_KEYS:
                        st.session_state.is_authenticated = True
                        st.success("✅ Access Granted! Please wait...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid Key! Contact Mitradnya Publication's to purchase a key.")
            else:
                st.info("⚠️ Instruction: Please enter your correct details and the Exam PIN provided by Mitradnya Publication's.")
                student_name = st.text_input("👤 Full Name (e.g., Rahul Patil):")
                student_div = st.text_input("🏫 Division (A/B/C):")
                student_roll = st.text_input("🔢 Roll No (Numbers Only):")
                student_email = st.text_input("📧 Email ID (For Result):")
                exam_pin_input = st.text_input("🔑 Exam PIN (Secret Password):", type="password")
                
                st.markdown("---")
                if st.button("🟢 Start Test", use_container_width=True):
                    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+$"
                    is_valid_email = re.match(email_pattern, student_email)
                    is_valid_roll = student_roll.isdigit()
                    valid_domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@rediffmail.com"]
                    is_real_domain = any(student_email.lower().endswith(d) for d in valid_domains)
                    
                    if not student_name or not student_div or not student_roll or not student_email or not exam_pin_input:
                        st.warning("⚠️ Please fill in all the details, including the Exam PIN.")
                    elif not is_valid_roll:
                        st.error("❌ Invalid Roll No! Please enter numbers only (e.g., 15).")
                    elif not is_valid_email or not is_real_domain:
                        st.error("❌ Fake Email Detected! Please use a real valid email address.")
                    elif exam_pin_input != SECRET_EXAM_PIN:
                        st.error("❌ Incorrect Exam PIN! You cannot start the test without the correct password.")
                    else:
                        st.session_state.test_status = 'in_progress'
                        st.rerun()
                    
        with tab2:
            st.markdown("<h3 style='font-size:22px;'>📖 Mitradnya's Interactive Study Room</h3>", unsafe_allow_html=True)
            if str(selected_chapter) == "1" or "Final Accounts" in str(selected_chapter): 
                try:
                    tools_df = pd.read_csv('Tools.csv', encoding='utf-8')
                    tools_df.columns = tools_df.columns.str.strip()
                    adjustment_list = tools_df['Topic_Name'].tolist()
                    
                    FREE_ADJS = ["Additional Capital", "Bad Debts"]
                    st.info(f"💡 Demo Access: You can view '{FREE_ADJS[0]}' and '{FREE_ADJS[1]}' for free.")
                    selected_adj = st.selectbox("🔍 Select Adjustment to Study & Practice:", adjustment_list)
                    
                    if selected_adj not in FREE_ADJS and not st.session_state.is_authenticated:
                        st.error("🔒 Premium Content Locked")
                        st.warning(f"⚠️ The visualization and interactive calculator for **{selected_adj}** are locked.")
                        study_key = st.text_input("🔑 Enter Premium Key:", key="study_key", type="password")
                        if st.button("Unlock Study Room 🚀"):
                            if study_key in VALID_KEYS:
                                st.session_state.is_authenticated = True
                                st.success("✅ Access Granted! Please wait...")
                                st.rerun()
                            else:
                                st.error("❌ Invalid Key! Contact Mitradnya Publication's to purchase a key.")
                    else:
                        adj_data = tools_df[tools_df['Topic_Name'] == selected_adj].iloc[0]
                        image_filename = str(adj_data['Image_File']).strip()
                        img_file = f"Images/{image_filename}"
                        img_file_alt = f"images/{image_filename}"
                        
                        st.markdown("---")
                        if os.path.exists(img_file):
                            st.image(img_file, caption=f"Visualization: {selected_adj} by Mitradnya Publication's", use_container_width=True)
                        elif os.path.exists(img_file_alt):
                            st.image(img_file_alt, caption=f"Visualization: {selected_adj} by Mitradnya Publication's", use_container_width=True)
                        else:
                            st.error("⚠️ Image Not Found in the system.")
                            st.warning(f"🔎 System checked for: **`{img_file}`**")
                            
                        st.markdown("---")
                        st.markdown(f"### 🎮 Interactive Calculator: {selected_adj}")
                        try:
                            import calculators
                            calculators.run_calculator(selected_adj)
                        except Exception:
                            st.warning("⏳ The selected adjustment is not yet added to the calculator.")
                except Exception as e:
                    st.error(f"⚠️ Error loading Tools.csv: {e}")
            elif str(selected_chapter) == "2" or "NPO" in str(selected_chapter):
                st.info("💡 **Topic: Not for Profit Concern (NPO)**")
                st.warning("⏳ Thanks for Visit!!! 🙏. This section will be Updated Very Soon!!! 🚀. Stay tuned to Mitradnya Publication's!!! 🎓")
            else:
                st.info(f"💡 **Topic: Chapter {selected_chapter}**")
                st.warning("⏳ Thanks for Visit!!! 🙏. This section will be Updated Very Soon!!! 🚀. Stay tuned to Mitradnya Publication's!!! 🎓")

        # ==========================================
        # Tab 3: Categorized Q&A with AI Solution
        # ==========================================
        with tab3:
        if qna_df is not None:
            cat_tabs = st.tabs(["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"])
            categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
            
            for i, cat_tab in enumerate(cat_tabs):
                with cat_tab:
                    filtered_df = qna_df[
                        (qna_df['Chapter_Name'].str.contains(str(selected_chapter), case=False, na=False)) & 
                        (qna_df['Category'].str.strip() == categories[i])
                    ]
                    
                    if not filtered_df.empty:
                        for idx, row in filtered_df.iterrows():
                            # येथे पूर्ण प्रश्न दिसेल
                            with st.expander(f"Question: {row['Question_Text'][:40]}..."):
                                st.markdown("### 📝 Full Problem Statement:")
                                st.write(row['Question_Text'])
                                
                                if st.button("🧠 Generate Solution", key=f"btn_{i}_{idx}"):
                                    with st.spinner("⏳ AI is calculating..."):
                                        try:
                                            model = genai.GenerativeModel('gemini-3.5-flash')
                                            response = model.generate_content(f"Solve this accountancy problem in Tally format: {row['Question_Text']}")
                                            st.markdown(response.text)
                                        except Exception as e:
                                            st.error(f"AI Error: {e}")
                    else:
                        st.info("या विभागात अजून प्रश्न नाहीत.")
        else:
            st.error("डेटा फाईल्स सापडल्या नाहीत!")
                                                                
                                    # 🧠 AI Solution Generator Button
                                    if st.button(f"🧠 Generate Solution", key=f"ai_{cat_name}_{q_idx}"):
                                        with st.spinner("⏳ Getting Solution..."):
                                            try:
                                                model = genai.GenerativeModel('gemini-3.5-flash')
                                                prompt = f"Solve this Accountancy problem in Tally ERP table format: {full_question_text}"
                                                response = model.generate_content(prompt)
                                                st.success("✅ Solution Generated!")
                                                st.markdown(response.text)
                                            except Exception as e:
                                                st.error(f"❌ AI Error: {e}")
                        else:
                            st.info(f"Will Update Soon!")
            else:
                st.error("⚠️ Failed to load QnA data.")                
        with tab4:
            st.markdown("<h3 style='font-size:22px;'>📄 Board Papers & Detailed Solutions</h3>", unsafe_allow_html=True)
            st.info("💡 **Previous Year Papers & Model Answers**")
            st.warning("⏳ Thanks for Visit!!! 🙏. This section will be Updated Very Soon!!! 🚀. Stay tuned to Mitradnya Publication's!!! 🎓")

    # ==========================================
    # Exam In Progress & Submit Logic
    # ==========================================
    elif st.session_state.test_status == 'in_progress':
        test_id = f"{selected_chapter}_{selected_part}".replace(" ", "_")
        
        timer_code = f"""
        <div style="background-color: #4F46E5; color: white; padding:10px; border-radius:8px; text-align:center; font-size:22px; font-weight:bold; font-family:sans-serif; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
            <span id="time">Loading Timer...</span>
        </div>
        <script>
            var testId = "{test_id}";
            var endTime = sessionStorage.getItem("examEndTime_" + testId);
            
            if (!endTime) {{
                endTime = new Date().getTime() + 20 * 60 * 1000; 
                sessionStorage.setItem("examEndTime_" + testId, endTime);
            }}
            
            var elem = document.getElementById('time');
            var timerId = setInterval(function() {{
                var now = new Date().getTime();
                var distance = endTime - now;
                
                if (distance <= 0) {{
                    clearInterval(timerId);
                    elem.innerHTML = "⚠️ Time Up! Please submit your exam immediately.";
                    elem.parentElement.style.backgroundColor = "#E74C3C";
                }} else {{
                    var m = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                    var s = Math.floor((distance % (1000 * 60)) / 1000);
                    elem.innerHTML = "⏱️ Time Remaining: " + m + " m " + s + " s";
                }}
            }}, 1000);
        </script>
        """
        components.html(timer_code, height=70)
        
        user_answers = []
        for idx, (i, row) in enumerate(current_quiz_df.iterrows(), 1):
            st.write(f"**Q {idx}. {row['Question']}**")
            
            raw_options = [str(row['Option A']), str(row['Option B']), str(row['Option C']), str(row['Option D'])]
            unique_options = []
            for opt in raw_options:
                while opt in unique_options:
                    opt += " "  
                unique_options.append(opt)
            options = unique_options
            
            random.seed(i)
            random.shuffle(options)
            random.seed()
            
            ans = st.radio("Options:", options, key=f"q_{i}", index=None, label_visibility="collapsed")
            user_answers.append(ans)
            st.write("")

        if st.button("🚀 Submit Exam", type="primary", use_container_width=True):
            if None not in user_answers:
                score = 0
                detailed_report_text = ""
                correct_answers = current_quiz_df['Correct Answer (Full Text)'].astype(str).str.strip().values
                results_list = []
                
                for idx, (i, row) in enumerate(current_quiz_df.iterrows()):
                    user_ans = str(user_answers[idx]).strip()
                    correct_ans = str(correct_answers[idx]).strip()
                    
                    if user_ans == correct_ans:
                        score += 1
                        status = "✅ Correct"
                        is_correct = True
                    else:
                        status = f"❌ Wrong (Correct: {correct_ans})"
                        is_correct = False
                        
                    detailed_report_text += f"Q: {row['Question']}\nYour Ans: {user_ans}\nStatus: {status}\n\n"
                    results_list.append({'q': row['Question'], 'user_ans': user_ans, 'correct_ans': correct_ans, 'is_correct': is_correct})
                
                with st.spinner("Saving data to Excel..."):
                    GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbw3wvGw7hDYyAQIKBL1Rd-jTCP8DwzLzGGITCKTZwbCDMXaInzi3t2vyU4ipzz9SM9-/exec"
                    
                    safe_name = urllib.parse.quote(str(student_name))
                    safe_div = urllib.parse.quote(str(student_div))
                    safe_roll = urllib.parse.quote(str(student_roll))
                    safe_test = urllib.parse.quote(f"{selected_chapter} - {selected_part}")
                    safe_score = urllib.parse.quote(str(score))
                    safe_email = urllib.parse.quote(str(student_email))  
                    
                    final_url = f"{GOOGLE_SHEET_URL}?name={safe_name}&div={safe_div}&roll={safe_roll}&test={safe_test}&score={safe_score}&email={safe_email}"
                    
                    try:
                        res = requests.get(final_url)
                        sheet_success = (res.status_code == 200)
                    except Exception:
                        sheet_success = False
                
                send_detailed_email(TEACHER_EMAIL, student_name, student_div, student_roll, score, len(current_quiz_df), selected_chapter, selected_part, detailed_report_text, True)
                
                email_sent = False
                if student_email:
                    email_sent = send_detailed_email(student_email, student_name, student_div, student_roll, score, len(current_quiz_df), selected_chapter, selected_part, detailed_report_text, False)
                
                st.session_state.score = score
                st.session_state.total_questions = len(current_quiz_df)
                st.session_state.sheet_success = sheet_success
                st.session_state.email_sent = email_sent
                st.session_state.student_email = student_email
                
                st.session_state.test_status = 'submitted'
                st.rerun() 
            else:
                st.warning("⚠️ Please answer all questions before submitting.")

    elif st.session_state.test_status == 'submitted':
        test_id = f"{selected_chapter}_{selected_part}".replace(" ", "_")
        components.html(f"<script>sessionStorage.removeItem('examEndTime_{test_id}');</script>", height=0)
        
        st.success(f"🎉 Final Score: {st.session_state.score} / {st.session_state.total_questions}")
        
        if st.session_state.sheet_success:
            st.info("📊 Your result has been successfully saved in the system.")
            
        if st.session_state.student_email and st.session_state.email_sent:
            st.success(f"📧 The detailed Answer Key has been sent securely to your email: {st.session_state.student_email}")
            
        st.markdown("---")
        st.warning("🔒 Please check your registered email inbox to view your Detailed Result.")
        st.markdown("---")
        
        if st.button("🔄 Take Another Test", use_container_width=True):
            st.session_state.test_status = 'not_started'
            st.rerun()

    st.markdown("<br><hr><p style='text-align: center; color: var(--text-color); font-size: 16px;'>Developed with ❤️ by <b>Mitradnya Publication's (9422152294)</b></p>", unsafe_allow_html=True)
