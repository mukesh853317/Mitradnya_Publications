import streamlit as st
import pandas as pd
import os

def parse_table(lines):
    parsed = []
    for line in lines:
        # '|' ने स्प्लिट करा
        parts = [p.strip() for p in line.split('|')]
        # रिकामे कॉलम्स काढून टाका
        parts = [p for p in parts if p != '']
        if len(parts) >= 2:
            parsed.append(parts)

    if not parsed:
        return None

    # पहिले रो 'Header' म्हणून घ्या
    header = parsed[0]
    data = parsed[1:]
    
    # कॉलमची संख्या जुळवून घ्या
    max_cols = len(header)
    clean_data = []
    for row in data:
        if len(row) < max_cols:
            row = row + [''] * (max_cols - len(row))
        clean_data.append(row[:max_cols])
        
    return pd.DataFrame(clean_data, columns=header)

def show_student_dashboard():
    st.subheader("🎓 Student Dashboard")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')

    if not os.path.exists(csv_path):
        st.error("QnA.csv File Not Found!")
        return

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    df = df.ffill() # डेटा क्लीन करा

    categories = ["Short_Notes", "Exercise_Problems", "Extra_Practical"]
    tab_names = ["📖 Short Notes", "📝 Exercise Problems", "📊 Extra Practical"]
    tabs = st.tabs(tab_names)

    for i, tab in enumerate(tabs):
        with tab:
            cat_df = df[df['Category'].str.strip() == categories[i]]
            if cat_df.empty:
                st.info("No questions available.")
                continue

            # ग्रुपिंग करून प्रश्न दाखवणे
            for q_id, group in cat_df.groupby('Question_Text'): # साध्या ग्रुपिंगसाठी
                group = group.reset_index(drop=True)
                main_q = group.loc[0, 'Question_Text']
                
                with st.container(border=True):
                    st.markdown(f"#### {main_q}")
                    
                    # डेटा आणि टेबल वेगळे करणे
                    table_lines = [str(line) for line in group['Question_Text'].tolist() if '|' in str(line)]
                    
                    if table_lines:
                        table_df = parse_table(table_lines)
                        if table_df is not None:
                            st.table(table_df) # टेबल फॉरमॅटमध्ये दिसेल

                    # उत्तर बटण
                    if not pd.isna(group.loc[0, 'Answer_or_Hint']):
                        if st.button(f"🔍 Show Solution", key=f"btn_{i}_{q_id}"):
                            st.success(group.loc[0, 'Answer_or_Hint'])
