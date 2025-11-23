from services.kb_service import get_collection
from services.cache_service import get_cache, set_cache
from services.llm_service import get_groq_client
from utils.logger import log_info, log_error, log_warning
import time
from services.semantic_cache_service import get_semantic_cache, save_semantic_cache
from services.embed_service import embedder

groq_client = get_groq_client()

SIMILARITY_TOP_K = 3

def _format_retrieved_docs(results):
    ids = results.get("ids", [[]])[0]
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    items = []
    for i, doc in enumerate(docs):
        mid = ids[i] if i < len(ids) else None
        meta = metas[i] if i < len(metas) else {}
        items.append({
            "id": mid,
            "title": meta.get("title") if isinstance(meta, dict) else "Untitled",
            "content": doc,
            "expiry_days": meta.get("expiry_days", 365)
        })
    return items


def query_index(question: str):
    start_time = time.time() 
    """Query ke Chroma + LLM, tapi sekarang dengan Redis caching 🚀"""
    cache_key = f"cache:query:{question.lower().strip()}"


 # 🔹 STEP 1: Coba ambil dari semantic cache dulu
    semantic_cached = get_semantic_cache(question)
    if semantic_cached:
        log_info(f"[CACHE HIT - SEMANTIC] Ambil hasil mirip dari semantic cache untuk: {question}")
        return semantic_cached
    

    # === 1️⃣ Cek cache Redis dulu ===
    cached = get_cache(cache_key)
    if cached:
        duration = time.time() - start_time
        log_info(f"[CACHE HIT - Literal] {question} | waktu eksekusi: {duration:.3f}s")
        return cached["answer"]

    # === 2️⃣ Kalau belum ada di cache, lanjut proses seperti biasa ===
    try:
        collection = get_collection()
    except Exception as e:
        return f"Gagal akses koleksi Chroma: {e}"

    print(f"=== DEBUG QUERY === Total dokumen Chroma sekarang: {collection.count()} ===")

    if collection.count() == 0:
        return "Belum ada data dalam basis pengetahuan. Silakan tambahkan dokumen dulu."

    try:
        q_embedding = embedder.get_text_embedding(question)
    except Exception as e:
        log_warning(f"[WARNING] Gagal buat embedding question: {e}")
        q_embedding = None

    try:
        if q_embedding is not None:
            results = collection.query(
                query_embeddings=[q_embedding],
                n_results=SIMILARITY_TOP_K,
                include=["documents", "metadatas"]
            )
        else:
            results = collection.query(
                query_texts=[question],
                n_results=SIMILARITY_TOP_K,
                include=["documents", "metadatas"]
            )
    except Exception as e:
        log_error(f"[ERROR] Query Chroma gagal: {e}")
        return "Terjadi kesalahan saat mencari dokumen."

    retrieved = _format_retrieved_docs(results)
    if not retrieved:
        return "Maaf, tidak ditemukan informasi relevan di knowledge base."

    context_parts = []
    for r in retrieved:
        ctx_title = r.get("title") or r.get("id")
        ctx_text = (r.get("content") or "")[:1000]
        context_parts.append(f"### {ctx_title}\n{ctx_text}\n")

    context = "\n".join(context_parts)
    if len(context) > 4000:
        context = context[:4000] + "\n...[dipotong agar muat token limit]..."

    if groq_client is not None:
        try:
            prompt = f"""
You are a helpful assistant that answers questions based ONLY on the following documents.
Do NOT invent facts. If the answer is not present, state you don't know.

Documents:
{context}

Question: {question}

Answer concisely in Indonesian (max ~200 words). Start with one short sentence summarizing whether the docs include the answer.
"""
            resp = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            text = resp.choices[0].message.content.strip()
        except Exception as e:
            log_warning(f"[WARNING] Groq LLM gagal dipanggil: {e}")
            text = "Tidak ada LLM aktif — fallback jawaban kosong."
    else:
        snippets = []
        for r in retrieved:
            snippets.append(f"- {r.get('title') or r.get('id')}: {(r.get('content') or '')[:300]}")
        text = "Tidak ada LLM aktif — berikut hasil dokumen teratas yang relevan:\n" + "\n".join(snippets)

# 🔹 Hitung TTL cache dinamis (ambil yang paling pendek)
    ttl_days = min([r.get("expiry_days", 365) for r in retrieved], default=365)
    ttl_seconds = ttl_days * 24 * 60 * 60

 # === 3️⃣ Simpan hasil ke cache literal Redis ===
    set_cache(cache_key, {"answer": text, "docs": [r["id"] for r in retrieved]}, expire=ttl_seconds)
    
    # 🔹 Simpan ke semantic cache redis
    save_semantic_cache(
        question,
        text,
        related_docs=[r["id"] for r in retrieved], 
        expiry_days=ttl_days
        )


    duration = time.time() - start_time
    log_info(f"[CACHE MISS] {question} | waktu eksekusi: {duration:.3f}s | TTL={ttl_days} hari")
    return text
