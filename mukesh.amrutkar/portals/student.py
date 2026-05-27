import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("📚 Study Room - Mitradnya Publication's")
    
    # पाथ (Path) सेट करणे
    csv_path = 'data/QnA.csv'
    
    # फाईल लोड करणे
    try:
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip() # स्पेस काढणे
        
        # रिकाम्या ओळी काढून टाकणे (KeyError टाळण्यासाठी)
        df = df.dropna(subset=['Subject', 'Chapter_Name'])

        # फिल्टरिंग
        subject = st.selectbox("Select Subject", df['Subject'].unique())
        chapter = st.selectbox("Select Chapter", df[df['Subject'] == subject]['Chapter_Name'].unique())
        
        # डेटा फिल्टर करणे
        filtered_df = df[(df['Subject'] == subject) & (df['Chapter_Name'] == chapter)]
        
        st.write(f"### {chapter} चे प्रश्न:")
        
        # टेबल स्वरूपात दाखवणे
        st.dataframe(
            filtered_df[['Category', 'Question_Text', 'Answer_or_Hint']], 
            use_container_width=True,
            hide_index=True
        )

        # फंक्शन व्याख्या
        def render_table_data(answer_text):
            if isinstance(answer_text, str) and '|' in answer_text:
                lines = answer_text.split('\n')
                table_data = [line.split('|') for line in lines if '|' in line]
                if table_data:
                    html = "<table style='width:100%; border: 1px solid #ddd; border-collapse: collapse;'>"
                    for row in table_data:
                        html += "<tr>" + "".join([f"<td style='border: 1px solid #ddd; padding: 5px;'>{col.strip()}</td>" for row_data in row for col in [row_data]]) + "</tr>"
                    html += "</table>"
                    st.markdown(html, unsafe_allow_html=True)
            else:
                st.write(str(answer_text))

    except Exception as e:
        st.error(f"डेटा लोड करताना अडचण आली: {e}")

    st.title("🎓 Student Portal")
    st.info("Portal is working successfully!")
