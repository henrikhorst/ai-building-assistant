import os
from PyPDF2 import PdfReader

def extract_pdf_content(pdf_path):
    """Extracts text from a single PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Failed to read {pdf_path}: {e}")
        return None


lbo_text = extract_pdf_content("BauO_SH_2024.pdf")