import pandas as pd
import random
from fpdf import FPDF

# CSV फाईल्स लोड करताना encoding handle करा
def load_csv(file_path):
    for enc in ["utf-8", "utf-8-sig", "latin1", "cp1252"]:
        try:
            return pd.read_csv(file_path, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {file_path}")

qna_df = load_csv("QnA.csv")          # Descriptive / Practical Problems
mcq_df = load_csv("All in one.csv")   # MCQ Questions with answers

def generate_descriptive_questions(df, chapters, num_questions=2):
    paper = []
    for chapter in chapters:
        # QnA.csv मध्ये Chapter_Name आहे
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
        # All in one.csv मध्ये Chapter नाव नाही, Subject आहे
        chapter_questions = df[df['Subject'].str.contains("BK", na=False) & df['Question'].notna()]
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
selected_chapters = ["Partnership Final Accounts"]

descriptive_part = generate_descriptive_questions(qna_df, selected_chapters, num_questions=2)
mcq_part = generate_mcq_questions(mcq_df, selected_chapters, num_questions=3)

export_to_pdf(descriptive_part, mcq_part, filename="HSC_Accountancy_Paper.pdf")
