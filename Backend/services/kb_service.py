import os
import json
import chromadb
import shutil
from uuid import uuid4
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


CHROMA_PATH = "./chroma_db"
JSON_PATH = "processed/structured.json"
UPLOAD_FOLDER = "./uploads"

# === Inisialisasi client ===
# chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
def get_client():
    """Selalu ambil client Chroma terbaru."""
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_collection():
    """Selalu ambil koleksi terbaru dari Chroma."""
    client = get_client()
    return client.get_or_create_collection("informasi_docs")


# === Embedding model (bisa diganti sesuai model RAG kamu) ===
embedder = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# --- Helper JSON ---
def _load_json():
    if not os.path.exists(JSON_PATH):
        return []
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_json(data):
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- List semua dokumen ---
def list_docs():
    return _load_json()

# --- Tambah dokumen baru (ke JSON + Chroma) ---
def add_doc(title, content):
    data = _load_json()
    doc_id = str(uuid4())

    # Simpan ke JSON
    new_entry = {"id": doc_id, "title": title, "content": content}
    data.append(new_entry)
    _save_json(data)

    # Simpan ke Chroma (lengkap metadata dengan doc_id)
    collection = get_collection()
    embedding = embedder.get_text_embedding(content)
    collection.add(
        ids=[doc_id],
        documents=[content],
        embeddings=[embedding],
        metadatas=[{"title": title, "doc_id": doc_id}]
    )

    return doc_id


# --- Hapus dokumen ---
def delete_doc(doc_id):
    data = _load_json()
    new_data = [d for d in data if d["id"] != doc_id]
    _save_json(new_data)

    collection = get_collection()
    try:
        # Hapus semua embedding yang punya metadata doc_id sesuai
        collection.delete(where={"doc_id": doc_id})
        print(f"[INFO] Dokumen {doc_id} dihapus dari Chroma & JSON.")
        debug_json_docs()
        debug_list_docs()
        print("[DEBUG] Metadata di Chroma sebelum hapus:", collection.get(include=["metadatas"]))

    except Exception as e:
        print(f"[WARNING] Gagal hapus dari Chroma: {e}")


# --- Debug: Cek isi koleksi Chroma ---
def debug_list_docs():
    collection = get_collection()
    all_docs = collection.get(include=["metadatas", "documents"])
    print(f"\n=== DEBUG: DOKUMEN DI CHROMA ===")

    ids = all_docs.get("ids", [])
    for i, doc_id in enumerate(ids):
        meta = all_docs["metadatas"][i] if i < len(all_docs["metadatas"]) else {}
        content = all_docs["documents"][i][:60] if all_docs["documents"][i] else ""
        print(f"{i+1}. {doc_id} | {meta} | {content}...")

    print("================================\n")



# --- Debug: Cek isi JSON ---
def debug_json_docs():
    if not os.path.exists(JSON_PATH):
        print("JSON tidak ditemukan.")
        return
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"\n=== DEBUG: DOKUMEN DI JSON ===")
    for i, d in enumerate(data):
        print(f"{i+1}. {d['id']} | {d['title']}")
    print("================================\n")

# --- Reset Knowledge Base ---
def clear_json():
    """Kosongkan file JSON."""
    _save_json([])

def clear_chroma():
    client = get_client()
    """Hapus dan buat ulang koleksi Chroma secara realtime."""
    try:
        
        client.delete_collection("informasi_docs")
        print("[INFO] Koleksi Chroma dihapus.")
    except Exception as e:
        print(f"[WARNING] Gagal hapus koleksi Chroma: {e}")

    # Buat ulang koleksi baru
    client.get_or_create_collection("informasi_docs")
    print("[INFO] Koleksi Chroma dibuat ulang.")

def clear_uploads():
    """Hapus semua file di folder uploads."""
    try:
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    except Exception as e:
        print(f"[WARNING] Gagal hapus folder uploads: {e}")

def reset_kb():

    clear_json()
    clear_chroma()
    clear_uploads()

    print("[INFO] Knowledge Base berhasil direset.")
    return True
