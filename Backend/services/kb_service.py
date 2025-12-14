import os
import json
import chromadb
from datetime import datetime
import shutil
from uuid import uuid4
from services.cache_service import clear_cache, cache
from services.semantic_cache_service import r as semantic_cache
from utils.logger import log_info, log_warning, log_error
from services.cache_service import clear_all_cache
from services.semantic_cache_service import clear_semantic_cache
from services.preprocess_service import clean_text
import time
from datetime import datetime
import pytz
from utils.extractName import extract_name_from_content

# CHROMA_PATH = "./chroma_db"
CHROMA_PATH = "./chroma_db"
JSON_PATH = "processed/structured.json"
UPLOAD_FOLDER = "./uploads"

tz = pytz.timezone("Asia/Jakarta")
created_at = datetime.now(tz).isoformat()


def get_client():
    return chromadb.PersistentClient(path=CHROMA_PATH) #inisialisasi klien ChromaDB

def get_collection():
    client = get_client()
    return client.get_or_create_collection("informasi_docs") #mengambil atau membuat koleksi baru bernama "informasi_docs"


# Helper JSON
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

# List semua dokumen
def list_docs():
    return _load_json()

# Tambah dokumen baru (ke JSON + Chroma)
def add_doc( content, source_file=None, category="lainnya"):
    from services.index_service import index_document # hindari circular import

    data = _load_json()
    doc_id = str(uuid4())

    # TTL by category
    category = category.lower()
    if  any(k in category for k in ["spmb", "penerimaan siswa baru", "ppdb"]):
        expiry_days = 90
    elif  any(k in category for k in ["prestasi", "extrakulikuler"]):
        expiry_days = 180
    else:
        expiry_days = 365

    new_entry = {
        "id": doc_id,
        "name": extract_name_from_content(content),
        "content": content,
        "source_file": source_file,
        "category": category,
        "expiry_days": expiry_days,
        "created_at": created_at
    }
    data.append(new_entry)
    _save_json(data)

    metadata = {
        "doc_id": doc_id,
        "name": extract_name_from_content(content),
        "source_file": source_file,
        "category": category,
        "expiry_days": expiry_days,
        "created_at": created_at,
    }

    index_document(
        doc_id=doc_id,
        content=content,
        metadata=metadata
    )
   
    log_info(f"[INFO] Dokumen '{doc_id}' ({category}) disimpan dengan TTL {expiry_days} hari.")
    return doc_id

# Hapus dokumen 
def delete_doc(doc_id):
    start = time.time()
    data = _load_json()
    new_data = [d for d in data if d["id"] != doc_id]
    _save_json(new_data)

    collection = get_collection()
    try:
        # Hapus semua embedding yang punya metadata doc_id sesuai
        collection.delete(where={"doc_id": doc_id})
        duration = time.time() - start
        log_info(f"[DELETE SUCCESS] doc_id={doc_id} | durasi={duration:.2f}s")
        # debug_json_docs()
        # debug_list_docs()

        meta = collection.get(include=["metadatas"])
        log_info(f"[DEBUG] Metadata di Chroma sebelum hapus: {meta}")


    except Exception as e:
        log_error(f"[DELETE FAILED] doc_id={doc_id} | error={e}")

    # Invalidate cache yang nyimpen ID dokumen ini
    invalidate_cache_for_deleted_doc(doc_id)
    return True

# invalidasi cache Redis otomatis kalau ada dokumen dihapus
def invalidate_cache_for_deleted_doc(doc_id):
    for key in cache.scan_iter("cache:*"):
        value = cache.get(key)
        if value and doc_id in value:
            clear_cache(key)
            log_info(f"[CACHE INVALIDATED] Cache '{key}' dihapus karena mengandung doc {doc_id}")

     # Hapus semantic cache yang nyimpen doc_id terkait
    for key in semantic_cache.scan_iter("semcache:*"):
        raw = semantic_cache.get(key)
        if not raw:
            continue
        try:
            data = json.loads(raw)  # decode JSON string
            related_docs = data.get("related_docs", [])
            if doc_id in related_docs:
                semantic_cache.delete(key)
                log_info(f"[CACHE INVALIDATED] Cache '{key}' dihapus (semantic) karena terkait doc {doc_id}")
        except Exception as e:
            log_warning(f"[WARNING] Gagal decode semantic cache di {key}: {e}")
            continue

# # Cek isi koleksi Chroma 
# def debug_list_docs():
#     collection = get_collection()
#     all_docs = collection.get(include=["metadatas", "documents"])
#     print(f"\n=== DEBUG: DOKUMEN DI CHROMA ===")

#     ids = all_docs.get("ids", [])
#     for i, doc_id in enumerate(ids):
#         meta = all_docs["metadatas"][i] if i < len(all_docs["metadatas"]) else {}
#         content = all_docs["documents"][i][:60] if all_docs["documents"][i] else ""
#         print(f"{i+1}. {doc_id} | {meta} | {content}...")

#     print("================================\n")

# # Cek isi JSON 
# def debug_json_docs():
#     if not os.path.exists(JSON_PATH):
#         print("JSON tidak ditemukan.")
#         return
#     with open(JSON_PATH, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     print(f"\nDOKUMEN DI JSON ")
#     for i, d in enumerate(data):
#         print(f"{i+1}. {d['id']} | {d['title']}")
#     print("================================\n")

# Reset Knowledge Base
def clear_json():
    """Kosongkan file JSON."""
    _save_json([])

def clear_chroma():
    client = get_client()
    """Hapus dan buat ulang koleksi Chroma secara realtime."""
    try:
        
        client.delete_collection("informasi_docs")
        log_info("[INFO] Koleksi Chroma dihapus.")
    except Exception as e:
        log_warning(f"[WARNING] Gagal hapus koleksi Chroma: {e}")

    # Buat ulang koleksi baru
    client.get_or_create_collection("informasi_docs")
    log_info("[INFO] Koleksi Chroma dibuat ulang.")

def clear_uploads():
    """Hapus semua file di folder uploads."""
    try:
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    except Exception as e:
        log_warning(f"[WARNING] Gagal hapus folder uploads: {e}")

def reset_kb():

    clear_json()
    clear_chroma()
    clear_uploads()
    clear_all_cache()
    clear_semantic_cache()

    log_info("[INFO] Knowledge Base berhasil direset.")
    return True
