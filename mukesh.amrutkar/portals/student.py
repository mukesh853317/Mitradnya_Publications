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
    df.columns = df.columns.str.strip()

    # रिकामे values fill
    df['Chapter_Name'] = df['Chapter_Name'].ffill()
    df['Category'] = df['Category'].ffill()
    df['Question_Text'] = df['Question_Text'].fillna('').astype(str).str.strip()
    df['Answer_or_Hint'] = df['Answer_or_Hint'].fillna('').astype(str).str.strip()

    # नवीन question detect करणे:
    # ज्या row ला Chapter_Name + Category आहे आणि Question_Text आहे ती main row
    df['is_main_question'] = (
        df['Chapter_Name'].notna() &
        df['Category'].notna() &
        (df['Question_Text'] != '')
    )

    df['Question_ID'] = df['is_main_question'].cumsum()

    categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
    tab_names = ["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"]
    tabs = st.tabs(tab_names)

    for i, tab in enumerate(tabs):
        with tab:
            cat_df = df[df['Category'].str.strip() == categories[i]]

            if cat_df.empty:
                st.info("No questions available.")
                continue

            grouped = cat_df.groupby('Question_ID', sort=False)

            for q_id, group in grouped:
                group = group.reset_index(drop=True)

                # main question
                main_question = group.iloc[0]['Question_Text']
                answer_hint = group.iloc[0]['Answer_or_Hint']

                st.markdown(f"### {main_question}")

                normal_lines = []
                table_data = []
                table_headers = None

                for idx in range(1, len(group)):
                    text = str(group.loc[idx, 'Question_Text']).strip()

                    if not text:
                        continue

                    if '|' in text:
                        parts = [p.strip() for p in text.split('|')]

                        # रिकामे trailing columns remove
                        while parts and parts[-1] == '':
                            parts.pop()

                        if len(parts) >= 2:
                            if table_headers is None:
                                table_headers = parts
                            else:
                                table_data.append(parts)
                    else:
                        normal_lines.append(text)

                # Text भाग proper format मध्ये
                for line in normal_lines:
                    low = line.lower()

                    if "trial balance" in low:
                        st.markdown(f"**{line}**")

                    elif "adjustment" in low:
                        st.markdown("**Adjustments:**")

                    elif line[:2].isdigit() or (
                        len(line) > 1 and line[0].isdigit() and line[1] == '.'
                    ):
                        st.markdown(f"- {line}")

                    else:
                        st.write(line)

                # Table render
                if table_headers and table_data:
                    valid_rows = [row for row in table_data if len(row) == len(table_headers)]
                    if valid_rows:
                        tb_df = pd.DataFrame(valid_rows, columns=table_headers)
                        st.table(tb_df)

                # Answer / Hint
                if answer_hint:
                    if st.button("🔍 Show Answer / Hint", key=f"btn_{i}_{q_id}"):
                        st.success(answer_hint)

                st.divider()
