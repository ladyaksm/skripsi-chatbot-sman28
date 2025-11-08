import os
import docx
import mimetypes
import fitz  # PyMuPDF buat ekstraksi PDF text-based
from flask import jsonify
import pdfplumber
import json

# def extract_text(filepath: str) -> str:
   
#     mime_type, _ = mimetypes.guess_type(filepath)

#     # --- PDF text-based ---
#     if mime_type == "application/pdf":
#         text = ""
#         with fitz.open(filepath) as pdf:
#             for page in pdf:
#                 text += page.get_text("text")
#         return text.strip()

#    # --- Word Document ---
#     elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         doc = docx.Document(filepath)
#         text = "\n".join([para.text for para in doc.paragraphs])
#         return text.strip()
    
#     # --- File text biasa ---
#     elif mime_type == "text/plain" or filepath.lower().endswith(".txt"):
#         with open(filepath, "r", encoding="utf-8") as f:
#             return f.read().strip()

#     else:
#         raise ValueError("Format file tidak didukung. Hanya PDF , Word, TXT text-based.")


def extract_text(filepath: str) -> str:
    import mimetypes
    import fitz
    import pdfplumber
    import docx

    mime_type, _ = mimetypes.guess_type(filepath)
    text = ""

    # --- PDF ---
    if mime_type == "application/pdf":
        # Ambil teks biasa dulu
        with fitz.open(filepath) as pdf:
            for page in pdf:
                text += page.get_text("text")

        #  Coba ambil tabel juga
        try:
            with pdfplumber.open(filepath) as pdf:
                table_texts = []
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        headers = table[0]
                        for row in table[1:]:
                            row_data = dict(zip(headers, row))
                            # ubah ke format kalimat biar gampang diproses
                            row_str = ", ".join(f"{k}: {v}" for k, v in row_data.items() if v)
                            table_texts.append(row_str)
                if table_texts:
                    text += "\n\n" + "\n".join(table_texts)
                    print(f"[INFO] {len(table_texts)} baris tabel berhasil diekstrak dari {filepath}")
        except Exception as e:
            print(f"[WARNING] Gagal ekstrak tabel dari PDF: {e}")

        print(f"[DEBUG] OCR result length: {len(text.strip())}")
        print(f"[DEBUG] OCR snippet: {text[:300]}")


        return text.strip()

    # --- Word Document ---
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()

    # --- File teks biasa ---
    elif mime_type == "text/plain" or filepath.lower().endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()

    else:
        raise ValueError("Format file tidak didukung. Hanya PDF, Word, TXT text-based.")
