import streamlit as st
import pandas as pd
import os
import math
import datetime

def load_objective_test(selected_subject, selected_chapter):
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Objectives.csv')

    if not os.path.exists(csv_path):
        st.warning("⏳ Objective Questions will be updated soon! (Stay Tuned)")
        return

    df = pd.read_csv(csv_path)
    
    df_filtered = df[df['No'].astype(str).str.strip() == str(selected_chapter).strip()].reset_index(drop=True)

    if df_filtered.empty:
        st.info(f"💡 Objective test for '{selected_chapter}' is not available yet.")
        return

    total_questions = len(df_filtered)
    questions_per_set = 20

    st.markdown(f"<h3 style='color: #1e3a8a; margin-top: 0;'>🎯 MCQ Practice Test</h3>", unsafe_allow_html=True)

    if total_questions > questions_per_set:
        num_sets = math.ceil(total_questions / questions_per_set)
        
        set_options = []
        for i in range(num_sets):
            start_num = i * questions_per_set + 1
            end_num = min((i + 1) * questions_per_set, total_questions)
            set_options.append(f"📝 Test Set {i+1} (Questions {start_num} to {end_num})")
        
        selected_set_str = st.selectbox("🎯 Choose Test Set:", set_options)
        set_idx = set_options.index(selected_set_str)
        
        start_idx = set_idx * questions_per_set
        end_idx = min(start_idx + questions_per_set, total_questions)
        df_to_display = df_filtered.iloc[start_idx:end_idx].reset_index(drop=True)
    else:
        df_to_display = df_filtered
        set_idx = 0

    st.markdown("<hr style='margin: 5px 0 15px 0;'>", unsafe_allow_html=True)
    
    with st.form(key=f"quiz_form_{selected_chapter}_{set_idx}"):
        user_answers = {}
        
        for idx, row in df_to_display.iterrows():
            actual_q_no = (set_idx * questions_per_set + idx + 1) if total_questions > questions_per_set else (idx + 1)
            
            q_text = row['Question']
            options = [str(row['Option A']), str(row['Option B']), str(row['Option C']), str(row['Option D'])]
            
            st.markdown(f"**Q.{actual_q_no} : {q_text}**")
            
            user_answers[idx] = st.radio(
                "Choose the correct option:", 
                options, 
                key=f"q_{selected_chapter}_{actual_q_no}", 
                index=None
            )
            st.markdown("<hr style='margin: 10px 0; border-top: 1px dashed #eee;'>", unsafe_allow_html=True)
            
        submit_btn = st.form_submit_button("✅ Submit Test", type="primary")
        
        if submit_btn:
            score = 0
            questions_in_this_set = len(df_to_display)
            
            st.markdown("### 📊 Test Results:")
            
            for idx, row in df_to_display.iterrows():
                actual_q_no = (set_idx * questions_per_set + idx + 1) if total_questions > questions_per_set else (idx + 1)
                correct_ans = str(row['Correct Answer (Full Text)']).strip()
                selected_ans = str(user_answers[idx]).strip() if user_answers[idx] else "Not Selected"
                
                if selected_ans == correct_ans:
                    score += 1
                    st.success(f"✔️ **Q.{actual_q_no}:** Correct Answer! 🎉")
                else:
                    st.error(f"❌ **Q.{actual_q_no}:** Incorrect Answer! \n* Your Answer: {selected_ans} \n* Correct Answer: **{correct_ans}**")
            
            st.markdown("---")
            percentage = round((score / questions_in_this_set) * 100, 2)
            
            if score == questions_in_this_set:
                st.balloons() 
                st.success(f"🏆 **Excellent! Your Final Score: {score} / {questions_in_this_set} ({percentage}%)**")
            else:
                st.info(f"🏆 **Your Final Score: {score} / {questions_in_this_set} ({percentage}%)**")
                
            # 🔴 मुख्य बदल: विद्यार्थ्यांचे मार्क्स 'data/results.csv' मध्ये सेव्ह करणे
            try:
                results_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'results.csv')
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                
                new_report = pd.DataFrame([{
                    "Subject": str(selected_subject),
                    "Chapter": str(selected_chapter),
                    "Score": int(score),
                    "Total": int(questions_in_this_set),
                    "Percentage": float(percentage),
                    "Date": current_time
                }])
                
                if os.path.exists(results_path):
                    res_df = pd.read_csv(results_path)
                    res_df = pd.concat([res_df, new_report], ignore_index=True)
                    res_df.to_csv(results_path, index=False)
                else:
                    os.makedirs(os.path.dirname(results_path), exist_ok=True)
                    new_report.to_csv(results_path, index=False)
                    
                st.toast("📈 Progress saved successfully! Check 'My Progress' tab.", icon="✅")
            except Exception as e:
                st.error(f"Could not save progress to file: {e}")
