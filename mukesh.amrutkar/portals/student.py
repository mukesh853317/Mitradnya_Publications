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
        st.subheader("🎓 Student's Dashboard - Mitradnya Publication's 🎓")
        st.subheader("🎓 Student's Dashboard - Mitradnya Publication")

# API Key एकदाच सेट करा 
# योग्य पद्धतीने धडे फिल्टर करणे
    chapter_list = all_chapters_df[all_chapters_df['Subject'].astype(str) == str(selected_subject)]['Chapter_Name'].dropna().astype(str).unique().tolist()
    
    # इथे कोणतीही ड्युप्लिकेट की (key) नाही याची खात्री केली आहे
    selected_chapter = st.selectbox("Select Chapter", chapter_list, key="global_chapter_select_student")
    
    # 🔴 इथे धड्यानुसार डेटा अचूक फिल्टर होतो (त्यामुळे धडे मिक्स होत नाहीत)
df_filtered = df[(df['Subject'].astype(str).str.strip() == str(selected_subject).strip()) & 
(df['Chapter_Name'].astype(str).str.strip() == str(selected_chapter).strip())]

# १. Study Room 
# ==========================================
with main_tabs[0]:
        categories = ["IMP_Proforma", "Short_Notes", "Exercise_Problems", "Extra_Practical"]
        sub_tab_names = ["📑 IMP Proforma & Journal Entries", "📖 Short Notes & One Sentence", "📝 Exercise Problems", "📊 Extra Practical"]
        # 🔴 नवीन कॅटेगरी ॲड केली: One_Sentence
        categories = ["IMP_Proforma", "Short_Notes", "One_Sentence", "Exercise_Problems", "Extra_Practical"]
        sub_tab_names = ["📑 IMP Proforma", "📖 Short Notes", "📝 One Sentence Answers", "📝 Exercise Problems", "📊 Extra Practical"]
sub_tabs = st.tabs(sub_tab_names)

for i in range(len(categories)):
    main_title = str(first_row.get('Question_Text', ''))
    display_title = main_title[:80] + "..." if len(main_title) > 80 else main_title
    with st.expander(f" {display_title}"): # Removed Q. Prefix for cleaner look, optional based on choice
        with st.expander(f" {display_title}"):
            table_data = []
            answer_text = ""
            
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
                                
                            # 🔴 Short_Notes आणि One_Sentence ला टेबलमध्ये न टाकता थेट टेक्स्टमध्ये दाखवा
                            if cat_name in ["Short_Notes", "One_Sentence"]:
                                if line:
                                    st.markdown(line)
                                    st.markdown(f"{line}")
                            else:
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
                        if cat_name not in ["Short_Notes", "One_Sentence"] and table_data:
html_table = "<table style='width:100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom:10px;'>"
for r_idx, t_row in enumerate(table_data):
html_table += "<tr>"

st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

                        # 🔴 फक्त IMP_Proforma सोडून इतर सर्व टॅबला Solution बटण दाखवा
if cat_name != "IMP_Proforma":
if st.button("🧠 Generate Solution", key=f"btn_{cat_name}_{q_idx}", type="primary"):
if answer_text:

with st.spinner("⏳ Generating Solutions..."):
try:
    model = genai.GenerativeModel('gemini-3.5-flash') 
                                        
                                        # 🔴 मुख्य बदल: AI Prompt कॅटेगरीनुसार बदलणार!
                                        if cat_name == "Short_Notes":
                                            ai_prompt = f"You are an expert Commerce teacher for Maharashtra Board. Write a detailed, point-wise, and easy-to-understand short note on the following topic for a 12th standard student: '{q_text}'"
                                        elif cat_name == "One_Sentence":
                                            ai_prompt = f"You are an expert Commerce teacher. Provide a very clear, direct, and one-sentence answer for the following question: '{q_text}'"
                                        else:
                                            ai_prompt = f"You are an expert Commerce teacher. Solve this practical accountancy problem in detail step-by-step:\n\n{q_text}"
                                            
response = model.generate_content(f"Solve this accountancy problem in detail step-by-step:\n\n{q_text}", ai_prompt, stream=True, request_options={"timeout": 600}) key=f"dl_btn_{selected_year}")

                 
                               
bp_filtered = bp_df_sub[bp_df_sub['Year'].astype(str).str.strip() == str(selected_year).strip()]

for idx, row in bp_filtered.iterrows():
q_no = str(row.get('Question_No', f"{idx+1}"))
q_text = str(row.get('Question_Text', ''))
display_title = q_text[:80] + "..." if len(q_text) > 80 else q_text

with st.expander(f" Q.{q_no} : {display_title}"):
st.markdown(q_text.replace('\n', '<br>'), unsafe_allow_html=True)
st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

if st.button("🧠 Generate Solution", key=f"bp_btn_{selected_year}_{idx}", type="primary"):
with st.spinner("⏳ Generating Board Solution..."):
try:
model = genai.GenerativeModel('gemini-3.5-flash')
prompt = f"You are an expert commerce teacher for Maharashtra Board. Solve this board exam question in detail, step-by-step for the subject {selected_subject}:\n\n{q_text}"

response = model.generate_content(
prompt,
stream=True,
request_options={"timeout": 600}
)

st.markdown("### 📝 AI Generated Solution:")
