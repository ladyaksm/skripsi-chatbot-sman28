import re
import json
import nltk
import os
import uuid
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("indonesian"))

# === Helper: Load patterns eksternal ===
def load_patterns(pattern_file="patterns.json"):
    if not os.path.exists(pattern_file):
        print(f"[WARNING] File pattern.json tidak ditemukan: {pattern_file}")
        return {}
    with open(pattern_file, "r", encoding="utf-8") as f:
        return json.load(f)


# === Text Cleaning ===
def clean_text(text: str) -> str:
    """Cleaning dasar: lowercase, hapus karakter aneh, stopwords, spasi berlebih"""
    text = text.lower()
    text = re.sub(r"hhttp|httpp|nttps", "https", text)
    text = re.sub(r"[^a-z0-9\s.,]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [w for w in text.split() if w not in STOPWORDS]
    return " ".join(tokens)


# === Split Section Berdasarkan Patterns ===
def split_sections(text: str) -> list:
    sections = []
    patterns = load_patterns()  # Load otomatis

    for key, title in patterns.items():
        matches = re.findall(rf"({key}.*?)(?=\n===|\Z)", text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            clean_section = clean_text(match)
            sections.append({
                "id": str(uuid.uuid4()),
                "title": title,
                "content": clean_section
            })

    print(f"[DEBUG] Incoming text length: {len(text)}")
    print(f"[DEBUG] Available patterns: {list(patterns.keys())}")

    return sections


# === Simpan ke structured.json ===
def preprocess_to_json(raw_text: str, output_file="processed/structured.json") -> str:
    """Konversi teks ke format structured JSON dan simpan"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    sections = split_sections(raw_text)

    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.extend(sections)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    return output_file

def process_text(raw_text: str):
    sections = split_sections(raw_text)
    
    # kalau gak ada pattern match, simpan full text aja biar gak kosong
    if not sections and raw_text.strip():
        sections = [{
            "id": str(uuid.uuid4()),
            "title": "Full OCR Text",
            "content": clean_text(raw_text)
        }]
        print("[INFO] Tidak ada pattern cocok, seluruh teks disimpan sebagai 1 section.")
    
    return sections
