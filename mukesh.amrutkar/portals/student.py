import streamlit as st
import pandas as pd
import os

def parse_table(lines):
    parsed = []
    for line in lines:
        parts = [p.strip() for p in line.split('|')]
        parts = [p for p in parts if p != '']
        if len(parts) >= 2:
            parsed.append(parts)

    if not parsed:
        return None

    max_cols = max(len(r) for r in parsed)
    parsed = [r + [''] * (max_cols - len(r)) for r in parsed]
    return pd.DataFrame(parsed[1:], columns=parsed[0])

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard - Q&A Portal")

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')

    if not os.path.exists(csv_path):
        st.error("QnA.csv File Not Found!")
        return

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    df['Chapter_Name'] = df['Chapter_Name'].ffill()
    df['Category'] = df['Category'].ffill()
    df['Question_Text'] = df['Question_Text'].fillna('').astype(str).str.strip()
    df['Answer_or_Hint'] = df['Answer_or_Hint'].fillna('').astype(str).str.strip()

    df['is_main_question'] = df['Chapter_Name'].notna() & df['Category'].notna() & (df['Question_Text'] != '')
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

            for q_id, group in cat_df.groupby('Question_ID', sort=False):
                group = group.reset_index(drop=True)

                main_q = group.loc[0, 'Question_Text']
                answer_hint = group.loc[0, 'Answer_or_Hint']

                with st.container(border=True):
                    st.markdown(f"### {main_q}")

                    body_lines = group.loc[1:, 'Question_Text'].tolist()

                    text_lines = []
                    table_lines = []

                    for line in body_lines:
                        line = str(line).strip()
                        if not line:
                            continue
                        if '|' in line:
                            table_lines.append(line)
                        else:
                            text_lines.append(line)

                    for line in text_lines:
                        low = line.lower()

                        if "trial balance" in low:
                            st.markdown(f"**{line}**")
                        elif "adjustment" in low:
                            st.markdown("**Adjustments:**")
                        elif line[:2].strip().isdigit() or (len(line) > 1 and line[0].isdigit() and '.' in line[:3]):
                            st.markdown(f"- {line}")
                        else:
                            st.write(line)

                    if table_lines:
                        table_df = parse_table(table_lines)
                        if table_df is not None:
                            st.table(table_df)

                    if answer_hint:
                        if st.button("🔍 Show Answer / Hint", key=f"btn_{i}_{q_id}"):
                            st.success(answer_hint)

                st.write("")
