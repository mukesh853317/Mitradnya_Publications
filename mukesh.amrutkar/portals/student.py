import streamlit as st
import pandas as pd
import os

def show_student_dashboard():
    st.subheader("🎓 Mitradnya Publication's - Student Portal")
    
    # पाथ सेट करणे
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'QnA.csv')
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # जुन्या पद्धतीचे टॅब्स
        tab1, tab2, tab3 = st.tabs(["Short Notes", "Exercise", "Practical"])
        
        with tab1:
            st.write("### Short Notes")
            # फक्त प्रश्न दाखवणे (जसे तुम्हाला हवे होते)
            for index, row in df[df['Category'] == 'Short_Notes'].iterrows():
                st.write(f"**Q. {index+1}:** {row['Question_Text']}")
                st.divider()

        with tab2:
            st.write("### Exercise Problems")
            for index, row in df[df['Category'] == 'Exercise_Problems'].iterrows():
                st.write(f"**Q. {index+1}:** {row['Question_Text']}")
                st.divider()

        with tab3:
            st.write("### Extra Practical")
            for index, row in df[df['Category'] == 'Extra_Practical'].iterrows():
                st.write(f"**Q. {index+1}:** {row['Question_Text']}")
                st.divider()
    else:
        st.error("Data File is Not Found!")
