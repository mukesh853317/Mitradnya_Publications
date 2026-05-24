import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal")

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')

    if not os.path.exists(csv_path):
        st.error("QnA.csv File Not Found!")
        return

    df = pd.read_csv(csv_path)

    # Column names clean करणे
    df.columns = df.columns.str.strip()

    # Missing values fill करणे
    df['Chapter_Name'] = df['Chapter_Name'].ffill()
    df['Category'] = df['Category'].ffill()

    # Question text clean
    df['Question_Text'] = df['Question_Text'].fillna('').astype(str).str.strip()
    df['Answer_or_Hint'] = df['Answer_or_Hint'].fillna('').astype(str).str.strip()

    # ज्या row मध्ये "|" नाही तो main question
    df['is_main_question'] = ~df['Question_Text'].str.contains(r'\|', regex=True)

    # प्रत्येक main question ला unique id
    df['Question_ID'] = df['is_main_question'].cumsum()

    categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
    tab_labels = ["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"]

    tabs = st.tabs(tab_labels)

    for i, tab in enumerate(tabs):
        with tab:
            cat_df = df[df['Category'].str.strip() == categories[i]]

            if cat_df.empty:
                st.info(f"No data found for {categories[i]}")
                continue

            grouped = cat_df.groupby('Question_ID', sort=False)

            for q_id, group in grouped:
                main_rows = group[group['is_main_question']]
                table_rows = group[~group['is_main_question']]

                if main_rows.empty:
                    continue

                question_text = main_rows.iloc[0]['Question_Text']
                answer_text = main_rows.iloc[0]['Answer_or_Hint']

                st.markdown(f"### {question_text}")

                tb_data = []
                for _, row in table_rows.iterrows():
                    text = row['Question_Text']
                    parts = [p.strip() for p in text.split('|') if p.strip()]

                    if len(parts) == 3:
                        tb_data.append(parts)

                if tb_data:
                    tb_df = pd.DataFrame(
                        tb_data,
                        columns=["Particulars", "Debit ₹", "Credit ₹"]
                    )
                    st.table(tb_df)

                if answer_text:
                    if st.button("🔍 Show Answer / Hint", key=f"btn_{q_id}_{i}"):
                        st.success(f"**Solution / Hint:** {answer_text}")

                st.divider()
