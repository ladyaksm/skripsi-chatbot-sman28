from services.cache_service import get_cache, set_cache
from utils.logger import log_info, log_warning
import time
from services.semantic_cache_service import get_semantic_cache, save_semantic_cache
from services.llm_service import get_groq_client
from services.retrieval_service import retrieve_docs

# Inisialisasi klien Groq
groq_client = get_groq_client()

SIMILARITY_TOP_K = 5

def query_index(question: str):
    start_time = time.time() 
    cache_key = f"cache:query:{question.lower().strip()}"


 # ambil dari semantic cache dulu
    semantic_cached = get_semantic_cache(question)
    if semantic_cached:
        # log_info(f"[CACHE HIT - SEMANTIC] Ambil hasil mirip dari semantic cache untuk: {question}")
        return semantic_cached
    

    # Cek cache Redis 
    cached = get_cache(cache_key)
    if cached:
        duration = time.time() - start_time
        # log_info(f"[CACHE HIT - Literal] {question} | waktu eksekusi: {duration:.3f}s")
        return cached["answer"]
    
    # Jika tidak ada di cache, lakukan retrieval + LLM
    retrieved_nodes = retrieve_docs(question, SIMILARITY_TOP_K)

    if not retrieved_nodes:
        return "Informasi tidak ditemukan."

    ## Format context dari dokumen yang di-retrieve
    context_parts = []
    ids_found = []
    expiry_list = []

    for node in retrieved_nodes:
        meta = node.metadata or {} # ambil metadata dari node
        ids_found.append(meta.get("doc_id")) # simpan ID dokumen yang ditemukan
        expiry_list.append(meta.get("expiry_days", 365))

        context_parts.append(
            f"### {meta.get('name','Untitled')}\n{node.text[:1000]}\n"
        )

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
        for r in retrieved_nodes: # ambil snippet dari dokumen
            meta = r.metadata or {}
            snippets.append( 
                f"- {meta.get('name', 'Untitled')}: {r.text[:300]}" 
                ) 
        text = "Tidak ada LLM aktif — berikut hasil dokumen teratas yang relevan:\n" + "\n".join(snippets)


# TTL cache dinamis (ambil yang paling pendek)
    ttl_days = min(
        [(r.metadata or {}).get("expiry_days", 365) for r in retrieved_nodes],
        default=365
    )

    ttl_seconds = ttl_days * 24 * 60 * 60

    ids_found = [(r.metadata or {}).get("doc_id") for r in retrieved_nodes]
    set_cache(cache_key, {"docs": ids_found})

    save_semantic_cache(
        question, 
        text, 
        related_docs=ids_found, 
        expiry_days=ttl_days
        )

    duration = time.time() - start_time
    log_info(f"[CACHE MISS] {question} | waktu eksekusi: {duration:.3f}s | TTL={ttl_days} hari")
    return text

