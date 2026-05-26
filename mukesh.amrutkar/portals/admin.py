import pandas as pd
import random
from fpdf import FPDF

# CSV फाईल्स लोड करा
qna_file = "QnA.csv"          # Descriptive / Practical Problems
mcq_file = "All in one.csv"   # MCQ Questions with answers

qna_df = pd.read_csv(qna_file)
mcq_df = pd.read_csv(mcq_file)

def generate_descriptive_questions(df, chapters, num_questions=2):
    paper = []
    for chapter in chapters:
        chapter_questions = df[df['Chapter_Name'].str.contains(chapter, na=False)]
        if not chapter_questions.empty:
            selected = chapter_questions.sample(min(num_questions, len(chapter_questions)))
            for _, row in selected.iterrows():
                paper.append({
                    "question": row['Question_Text'],
                    "answer": row['Answer_or_Hint'] if 'Answer_or_Hint' in row and pd.notna(row['Answer_or_Hint']) else "Solution to be written"
                })
    return paper

def generate_mcq_questions(df, chapters, num_questions=2):
    paper = []
    for chapter in chapters:
        chapter_questions = df[df['Chapter'].str.contains(chapter, na=False)]
        if not chapter_questions.empty:
            selected = chapter_questions.sample(min(num_questions, len(chapter_questions)))
            for _, row in selected.iterrows():
                q = f"{row['Question']}\nA) {row['Option A']}\nB) {row['Option B']}\nC) {row['Option C']}\nD) {row['Option D']}"
                paper.append({
                    "question": q,
                    "answer": row['Correct Answer (Full Text)']
                })
    return paper

def export_to_pdf(descriptive, mcq, filename="Question_Paper.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="HSC Accountancy Question Paper", ln=True, align='C')
    pdf.ln(10)

    # Descriptive Questions
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Descriptive Questions", ln=True)
    pdf.set_font("Arial", size=11)
    for i, item in enumerate(descriptive, 1):
        pdf.multi_cell(0, 10, f"Q{i}. {item['question']}")
        pdf.multi_cell(0, 10, f"Answer Key: {item['answer']}")
        pdf.ln(5)

    # MCQ Questions
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="MCQ Questions", ln=True)
    pdf.set_font("Arial", size=11)
    for i, item in enumerate(mcq, 1):
        pdf.multi_cell(0, 10, f"Q{i}. {item['question']}")
        pdf.multi_cell(0, 10, f"Answer Key: {item['answer']}")
        pdf.ln(5)

    pdf.output(filename)
    print(f"PDF generated successfully: {filename}")

# वापर
selected_chapters = ["Partnership Final Accounts"]  # हव्या त्या chapters निवडा

descriptive_part = generate_descriptive_questions(qna_df, selected_chapters, num_questions=2)
mcq_part = generate_mcq_questions(mcq_df, selected_chapters, num_questions=3)

export_to_pdf(descriptive_part, mcq_part, filename="HSC_Accountancy_Paper.pdf")
