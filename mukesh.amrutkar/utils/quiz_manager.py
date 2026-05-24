import streamlit as st
import pandas as pd
import os

def load_objective_test(selected_chapter):
    # तुमची Objectives.csv फाईल
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Objectives.csv')

    if not os.path.exists(csv_path):
        st.warning("⏳ Objective Questions for this chapter will be uploaded soon! (Stay Tuned)")
        return

    # डेटा लोड करणे
    df = pd.read_csv(csv_path)
    
    # 🔴 महत्त्वाचा बदल: 'No' कॉलममध्ये चॅप्टरचे नाव/नंबर असल्याने त्यावरून फिल्टर करणे
    df_filtered = df[df['No'].astype(str).str.strip() == str(selected_chapter)].reset_index(drop=True)

    if df_filtered.empty:
        st.info(f"💡 No Objectives Test for this Chapter {selected_chapter} ")
        return

    st.markdown(f"<h3 style='color: #1e3a8a;'>🎯 MCQ Practice Test</h3>", unsafe_allow_html=True)
    
    # Streamlit Form चा वापर
    with st.form(key=f"quiz_form_{selected_chapter}"):
        user_answers = {}
        
        for idx, row in df_filtered.iterrows():
            q_no = idx + 1 # प्रश्नाचा नंबर आपोआप १, २, ३ असा येईल
            q_text = row['Question']
            options = [str(row['Option A']), str(row['Option B']), str(row['Option C']), str(row['Option D'])]
            
            st.markdown(f"**Q.{q_no} : {q_text}**")
            
            user_answers[idx] = st.radio(
                "Choose Right Option:", 
                options, 
                key=f"q_{selected_chapter}_{q_no}", 
                index=None
            )
            st.markdown("<hr style='margin: 15px 0; border-top: 1px dashed #ddd;'>", unsafe_allow_html=True)
            
        submit_btn = st.form_submit_button("✅ Submit Test", type="primary")
        
        if submit_btn:
            score = 0
            total_questions = len(df_filtered)
            
            st.markdown("### 📊 Test Results 📊:")
            
            for idx, row in df_filtered.iterrows():
                correct_ans = str(row['Correct Answer (Full Text)']).strip()
                selected_ans = str(user_answers[idx]).strip() if user_answers[idx] else "Not Selected"
                
                if selected_ans == correct_ans:
                    score += 1
                    st.success(f"✔️ **Q.{idx + 1}:** Correct Ans! 🎉")
                else:
                    st.error(f"❌ **Q.{idx + 1}:** Wrong Ans! \n* Your Ans: {selected_ans} \n* Correct Ans: **{correct_ans}**")
            
            st.markdown("---")
            if score == total_questions:
                st.balloons() 
                st.success(f"🏆 **Congratulations! Your Final Score: {score} / {total_questions}**")
            else:
                st.info(f"🏆 **Your Final Score: {score} / {total_questions}**")
