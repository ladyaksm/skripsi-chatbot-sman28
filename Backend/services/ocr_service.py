import os
import pdfplumber
import docx
import mimetypes
import fitz 
from flask import jsonify
from utils.logger import log_warning

def extract_text(filepath: str) -> str:
    mime_type, _ = mimetypes.guess_type(filepath)
    text = ""

    # untuk file PDF 
    if mime_type == "application/pdf":
        # Ambil teks biasa dulu
        with fitz.open(filepath) as pdf:
            for page in pdf:
                text += page.get_text("text")

        print(f"[DEBUG] result length: {len(text.strip())}")
        print(f"[DEBUG] snippet: {text[:300]}")

        return text.strip()

    # untuk file Word Document
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()

    else:
        raise ValueError("Format file tidak didukung. Hanya PDF, Word")
