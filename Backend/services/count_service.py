import json
import os

class CountService:
    def __init__(self, json_path="processed/structured.json"):
        self.json_path = json_path
        self.data = self._load_json()

    #  Load knowledge base JSON
    def _load_json(self):
        if not os.path.exists(self.json_path):
            return []
        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    #  Keyword detection
    COUNT_KEYWORDS = [
        "berapa", "jumlah", "total", 
        "ada berapa", "berapa banyak"
    ]

    CATEGORY_MAP = {
        "guru": "data guru",
        "karyawan": "data guru",   
        "prestasi": "data prestasi",
        "siswa berprestasi": "data prestasi",
        "eskul": "data extrakulikuler dan komunitas",
        "ekstrakurikuler": "data extrakulikuler dan komunitas"
    }

    def is_count_query(self, question: str):
        q = question.lower()
        return any(k in q for k in self.COUNT_KEYWORDS)

    #  Tentukan kategori dari query
    def detect_category(self, question: str):
        q = question.lower()
        for keyword, category in self.CATEGORY_MAP.items():
            if keyword in q:
                return category
        return None

    #  Hitung jumlah dokumen
    def count_by_category(self, category: str):
        return len([d for d in self.data if d.get("category") == category])

    #  ENTIRE PIPELINE
    def handle_count_query(self, question: str):
        if not self.is_count_query(question):
            return None  # bukan query hitung → lanjut ke LLM

        category = self.detect_category(question)
        if not category:
            return {
                "answer": "Kategori yang ditanyakan tidak dapat dikenali. Coba tanyakan lebih spesifik.",
                "type": "count"
            }

        total = self.count_by_category(category)

        return {
            "answer": f"Terdapat total {total} data pada kategori '{category}'."
        }
