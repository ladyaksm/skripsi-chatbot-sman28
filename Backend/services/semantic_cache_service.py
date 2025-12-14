import redis
import json
import numpy as np
from numpy.linalg import norm
from services.embed_service import embedder
import pickle
import base64
from utils.logger import log_info, log_warning

# Setup Redis connection
r = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)  # pakai DB 1 khusus semantic cache

# query spesifik nama
def should_skip_semantic(question: str) -> bool:
    keywords = ["nama", "bernama", "siapa"]
    return any(k in question.lower() for k in keywords)

# Helper cosine similarity 
def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (norm(a) * norm(b))

# Simpan ke cache (embedding + jawaban)
def save_semantic_cache(question, answer, related_docs=None, expiry_days=365):
    emb = embedder.get_text_embedding(question)

    # Encode embedding (biar nggak terlalu berat)
    encoded_emb = base64.b64encode(pickle.dumps(emb)).decode("utf-8")
    
    cache_data = {
        "q": question,
        "e": encoded_emb,
        "a": answer,
        "related_docs": related_docs or [],
        "expiry_days": expiry_days}
    
     # TTL dalam detik biar Redis otomatis hapus cache-nya
    ttl_seconds = expiry_days * 24 * 60 * 60
    r.setex(f"semcache:{question.lower().strip()}", ttl_seconds, json.dumps(cache_data))

    log_info(f"[SEMANTIC CACHE] Simpan cache untuk: {question}")

# Cek cache yang mirip
def get_semantic_cache(question, threshold=0.93):

     # Skip semantic cache untuk query spesifik nama
    if should_skip_semantic(question):
        print("[SKIP SEMCACHE] Query spesifik nama → cari ulang dokumen")
        return None
    
    new_emb = embedder.get_text_embedding(question)
    
    for key in r.scan_iter("semcache:*"):
        data = json.loads(r.get(key))
        try:
            # Decode embedding yang disimpen di key 'e'
            emb_bytes = base64.b64decode(data["e"])
            cached_emb = pickle.loads(emb_bytes)
        except Exception as e:
            log_warning(f"[WARNING] Gagal decode embedding di {key}: {e}")
            continue

        sim = cosine_similarity(new_emb, cached_emb)
        print(f"[DEBUG] sim({question[:20]} vs {data['q'][:20]}) = {sim:.3f}")
        if sim >= threshold:
            log_info(f"[SEMANTIC CACHE HIT] Pertanyaan '{question}' ≈ '{data['q']}' (sim={sim:.3f})")
            return data["a"]
    return None

# Hapus semua semantic cache 
def clear_semantic_cache():
    for key in r.scan_iter("semcache:*"):
        r.delete(key)
    log_info("[SEMANTIC CACHE] Semua cache semantic dihapus.")
