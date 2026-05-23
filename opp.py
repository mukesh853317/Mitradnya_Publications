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

# -----------------------------------------------------
# 1. Premium Access Setup (तुमचे सिक्रेट पासवर्ड्स)
# -----------------------------------------------------
VALID_KEYS = ["MITRADNYA-101", "MUKESH-PRO-2026", "VIP-STUDENT-99"]

# --- Page Config नेहमी सर्वात वर असावे ---
st.set_page_config(page_title="📚 Mitradnya Publication's Online Exam 📚", page_icon="📝", layout="centered")

if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

# -----------------------------------------------------
# 2. Mitradnya Publication - Setup
# -----------------------------------------------------
TEACHER_EMAIL = "vidyarthi.mitradnyapublications@gmail.com" 
try:
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
except:
    EMAIL_PASSWORD = "" 

TEACHER_NAME = "Mitradnya Publication's"
SECRET_EXAM_PIN = "MIT2026" 

@st.cache_data
def load_data():
    try:
        try:
            df = pd.read_csv('All in one.csv', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv('All in one.csv', encoding='cp1252')
        # रकान्यांच्या नावांमधील फालतू स्पेसेस काढून टाकण्यासाठी
        df.columns = df.columns.str.strip()
        df.fillna("None", inplace=True) 
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

df = load_data()

# --- QnA डेटा लोड करण्यासाठी नवीन सुरक्षित फंक्शन ---
@st.cache_data
def load_qna_data():
    try:
        try:
            qna_df = pd.read_csv('QnA.csv', encoding='utf-8', on_bad_lines='skip')
        except Exception:
            qna_df = pd.read_csv('QnA.csv', encoding='cp1252', on_bad_lines='skip')
        
        qna_df.columns = qna_df.columns.str.strip()
        qna_df.fillna("माहिती उपलब्ध नाही", inplace=True) 
        return qna_df
    except Exception as e:
        return None

qna_df = load_qna_data()

def send_detailed_email(receiver_email, student_name, div, roll, score, total, chapter, test_name, report_content, is_teacher=True):
    if is_teacher:
        subject = f"New Result: {student_name} ({div}-{roll}) - {score}/{total}"
        body = f"📚 Result Alert for Mitradnya Publication's!\n\nStudent: {student_name}\nDivision: {div}\nRoll No: {roll}\nChapter: {chapter}\nTest: {test_name}\nScore: {score}/{total}\n\n--- Detailed Report ---\n{report_content}"
    else:
        subject = f"Your Exam Result - (Mitradnya Publication's) ({score}/{total})"
        body = f"Dear {student_name},\n\nYou have successfully completed the online test.\n\nChapter: {chapter}\nTest: {test_name}\nYour Score: {score}/{total}\n\n--- Detailed Performance ---\n{report_content}\n\nKeep Studying!\n- Mitradnya Publication's"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = TEACHER_NAME
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(TEACHER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(TEACHER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True
    except: return False

# --- CUSTOM CSS (Premium EdTech Theme - Fixed Emojis) ---
st.markdown("""
    <style>
    /* 1. App Background - Very subtle modern gradient */
    .stApp {
        background-color: var(--background-color);
        background-image: radial-gradient(circle at top right, rgba(79, 70, 229, 0.05), transparent),
                          radial-gradient(circle at bottom left, rgba(6, 182, 212, 0.05), transparent);
    }

    /* 2. Scrolling News Ticker - Adapts to Dark/Light Mode */
    .news-ticker {
        background: linear-gradient(90deg, rgba(79, 70, 229, 0.1), rgba(6, 182, 212, 0.1));
        color: var(--text-color);
        padding: 12px;
        font-weight: 700;
        font-size: 16px;
        border-radius: 8px;
        border-left: 5px solid #4F46E5;
        margin-bottom: 20px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }

    /* 3. Main Title - Fixed Emoji Rendering */
    h1, h2, h3 { 
        color: var(--text-color) !important; /* डार्क/लाईट मोडमध्ये आपोआप ॲडजस्ट होईल आणि इमोजी रंगीत राहतील */
        text-align: center; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1 {
        font-size: 2.6em !important;
        font-weight: 900;
        margin-bottom: 0px;
        padding-bottom: 10px;
    }

    /* 4. Action Buttons (Modern Indigo) */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4F46E5, #3B82F6);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 10px rgba(79, 70, 229, 0.3);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(79, 70, 229, 0.5);
    }

    /* 5. Beautiful Transparent Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(128, 128, 128, 0.05);
        border-radius: 8px 8px 0px 0px;
        padding: 12px 20px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(79, 70, 229, 0.1);
        border-bottom: 3px solid #4F46E5;
    }
    /* Tab Text Color - explicitly handled to adapt */
    .stTabs [aria-selected="true"] div[data-testid="stMarkdownContainer"] p {
        color: #4F46E5 !important;
        font-weight: 800;
        font-size: 16px;
    }

    /* 6. Soft Card Effect for Options */
    div.stRadio > div, div.stInfo, div.stSuccess, div.stWarning, div.stError { 
        border-radius: 10px; 
        box-shadow: 0px 2px 10px rgba(0,0,0,0.04); 
    }
    div.stRadio > div {
        background-color: var(--secondary-background-color); 
        padding: 15px; 
        border-left: 5px solid #06B6D4; 
        transition: transform 0.2s ease;
    }
    div.stRadio > div:hover {
        transform: translateX(4px);
        border-left: 5px solid #4F46E5; 
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------
# Sidebar (साईडबार डिझाईन आणि हेडिंग)
# -----------------------------------------------------
st.sidebar.markdown("<h2 style='text-align: left; font-size: 22px;'> 📚Mitradnya Publication's📚 </h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# प्रीमियम स्टेटस दाखवणे
if st.session_state.is_authenticated:
    st.sidebar.success("🌟 Premium Access Active")
else:
    st.sidebar.warning("🔒 Free Version (Limited Access)")

if 'test_status' not in st.session_state:
    st.session_state.test_status = 'not_started' 

if df is not None:
    sidebar_disabled = st.session_state.test_status != 'not_started'
    
    # CSV मधील कॉलमचे अचूक नाव शोधणे ('No.' किंवा 'No')
    chapter_col = 'No.' if 'No.' in df.columns else 'No' if 'No' in df.columns else df.columns[0]
    
    chapters = df[chapter_col].unique()
    selected_chapter = st.sidebar.selectbox("1. Select Chapter:", chapters, disabled=sidebar_disabled)
    
    chapter_questions = df[df[chapter_col] == selected_chapter]
    total_q = len(chapter_questions)
    
    st.sidebar.markdown("---")
    
    chunk_size = 20
    test_parts = []
    for i in range(0, total_q, chunk_size):
        test_parts.append(f"Test {i//chunk_size + 1}")
        
    selected_part = st.sidebar.radio("2. Select Test Part:", test_parts, disabled=sidebar_disabled)
    
    part_index = test_parts.index(selected_part)
    start_idx = part_index * chunk_size
    end_idx = start_idx + chunk_size
    current_quiz_df = chapter_questions.iloc[start_idx:end_idx]
    
    st.title("📚 Mitradnya Publication's Online Portal 📚")
    
    # पळणारी न्यूज पट्टी (Marquee)
    st.markdown("<div class='news-ticker'><marquee behavior='scroll' direction='left' scrollamount='6'>🔥 Welcome to Mitradnya Publication's! | 🚀 Unlock Premium Features Today | 🎓 Best Study Material by Mitradnya Publication's | 📞 Need a Premium Key? Contact on: 9422152294</marquee></div>", unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='font-size: 20px;'>📘 Topic: Chapter {selected_chapter}</h3>", unsafe_allow_html=True)
    st.write(f"**{selected_part} (20 Marks / 20 Minutes)**")
    
    if st.session_state.test_status == 'not_started':
        
        # येथे ४ नवीन टॅब्स बनवले आहेत 
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Exam Portal", 
            "📖 Study Room", 
            "📓 Chapter Q & A", 
            "📄 Papers & Solutions"
        ])
        
        # ==========================================
        # टॅब १: परीक्षेचा भाग (Test Logic)
        # ==========================================
        with tab1:
            if selected_part != "Test 1" and not st.session_state.is_authenticated:
                st.error("🔒 Premium Test Locked")
                st.warning("⚠️ This test is for Premium Students only. 'Test 1' is available for free practice.")
                st.write("To unlock all tests, enter your Premium Access Key below:")
                
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
                    
        # ==========================================
        # टॅब २: अभ्यासाची खोली (Study Room)
        # ==========================================
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
                        st.write("To unlock all study materials and calculators, enter your Premium Access Key below:")
                        
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
                            st.image(img_file, caption=f"Visualization: {selected_adj} by Mitradnya Publication", use_container_width=True)
                        elif os.path.exists(img_file_alt):
                            st.image(img_file_alt, caption=f"Visualization: {selected_adj} by Mitradnya Publication", use_container_width=True)
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
        # टॅब ३: प्रश्न उत्तरे आणि प्रॅक्टिस (Chapter Q & A)
        # ==========================================
        with tab3:
        st.markdown("<h3 style='font-size:22px;'>📓 Chapter-wise Q&A and Practice Questions</h3>", unsafe_allow_html=True)
        st.info(f"💡 **Topic: Chapter {selected_chapter}**")
        if qna_df is not None:
            qna_chapter_col = 'No.' if 'No.' in qna_df.columns else qna_df.columns[0]
            chapter_qna = qna_df[qna_df[qna_chapter_col] == selected_chapter]
            if not chapter_qna.empty:
                st.write("---")
                for idx, row in chapter_qna.iterrows():
                    question_text = row.get('Question', f"प्रश्न {idx+1}")
                    answer_text = row.get('Answer', "Ans is not given.")
                    with st.expander(f"🔹 {question_text}"):
                        st.markdown(f"**Ans:** {answer_text}")
            else:
                st.warning("⏳ Questions for this chapter will be updated soon! (Stay Tuned)")
        else:
            st.error("⚠️ The QnA.csv file was not found in the system. Please check the file.")
           
        # ==========================================
        # टॅब ४: पेपर्स आणि सोल्युशन्स (Papers & Solutions)
        # ==========================================
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

