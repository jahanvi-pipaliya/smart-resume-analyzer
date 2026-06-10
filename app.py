import streamlit as st
import fitz  # pymupdf
from docx import Document

def extract_text_from_pdf(file):
    text = ""
    pdf_file = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf_file:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def load_skills():
    with open("skills.txt", "r") as f:
        return [line.strip().lower() for line in f.readlines()]

def match_skills(resume_text, skills_list):
    resume_text = resume_text.lower()
    found = [skill for skill in skills_list if skill in resume_text]
    return found

# --- Streamlit App ---
st.title("🧠 Smart Resume Analyzer")
st.write("Upload your resume and see how well it matches with popular job skills!")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)

    skills = load_skills()
    matched_skills = match_skills(text, skills)

    st.subheader("✅ Skills Found in Resume:")
    st.write(", ".join(matched_skills))

    st.subheader("📊 Match Score:")
    score = round(len(matched_skills) / len(skills) * 100, 2)
    st.write(f"{score}%")
    
    st.subheader("📄 Job Description Matching (Optional)")
job_description = st.text_area("Paste the job description here:")

if job_description:
    jd_keywords = [word.strip().lower() for word in job_description.split()]
    matched_jd = [word for word in jd_keywords if word in text.lower()]

    st.subheader("✅ Job Description Match:")
    st.write(f"{len(matched_jd)} out of {len(set(jd_keywords))} keywords found.")

    missing = [word for word in jd_keywords if word not in text.lower()]
    st.subheader("❌ Missing Keywords:")
    st.write(", ".join(set(missing[:15])) + " ...") if missing else st.success("All keywords covered!")


