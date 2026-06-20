import re
from pypdf import PdfReader
import docx

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX {docx_path}: {e}")
        return ""

def extract_text(filepath):
    lower_path = filepath.lower()
    if lower_path.endswith('.pdf'):
        return extract_text_from_pdf(filepath)
    elif lower_path.endswith('.docx'):
        return extract_text_from_docx(filepath)
    return ""