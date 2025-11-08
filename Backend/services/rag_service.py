# services/rag_service.py
import os
import json
import chromadb
from services.kb_service import get_collection
from config import GROQ_API_KEY

# Embedding model (yang sebelumnya juga dipakai)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embedder = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Optional: gunakan Groq client langsung bila tersedia
try:
    from groq import Groq as GroqClient
    GROQ_CLIENT_AVAILABLE = True
    groq_client = GroqClient(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
except Exception:
    GROQ_CLIENT_AVAILABLE = False
    groq_client = None

SIMILARITY_TOP_K = 3

def _format_retrieved_docs(results):
    """
    results: dict returned by collection.query(...) with keys 'ids','documents','metadatas'
    """
    ids = results.get("ids", [[]])[0]
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    items = []
    for i, doc in enumerate(docs):
        mid = ids[i] if i < len(ids) else None
        meta = metas[i] if i < len(metas) else {}
        items.append({
            "id": mid,
            "title": meta.get("title") if isinstance(meta, dict) else None,
            "content": doc
        })
    return items

def query_index(question: str):
    """
    New query flow:
    - embed question
    - query chroma with query_embeddings
    - assemble context (top-k docs)
    - (optional) call Groq LLM to answer using that context
    - fallback: return docs snippet if LLM unavailable
    """
    try:
        collection = get_collection()
    except Exception as e:
        return f"Gagal akses koleksi Chroma: {e}"

    # quick debug
    print(f"=== DEBUG QUERY === Total dokumen Chroma sekarang: {collection.count()} ===")

    if collection.count() == 0:
        return "Belum ada data dalam basis pengetahuan. Silakan tambahkan dokumen dulu."

    # 1) hitung embedding untuk pertanyaan
    try:
        q_embedding = embedder.get_text_embedding(question)
    except Exception as e:
        print(f"[WARNING] Gagal buat embedding question: {e}")
        q_embedding = None

    # 2) Query Chroma (prioritas: gunakan query_embeddings jika ada embedding)
    try:
        if q_embedding is not None:
            # query by embedding
            results = collection.query(
                query_embeddings=[q_embedding],
                n_results=SIMILARITY_TOP_K,
                include=["documents", "metadatas"]
            )
        else:
            # fallback: query by raw text (Chroma may support)
            results = collection.query(
                query_texts=[question],
                n_results=SIMILARITY_TOP_K,
                include=["documents", "metadatas"]
            )
    except Exception as e:
        print(f"[ERROR] Query Chroma gagal: {e}")
        return "Terjadi kesalahan saat mencari dokumen."

    # 3) format hasil
    retrieved = _format_retrieved_docs(results)
    if not retrieved:
        return "Maaf, tidak ditemukan informasi relevan di knowledge base."

    # 4) buat context prompt
    context_parts = []
    for r in retrieved:
        ctx_title = r.get("title") or r.get("id")
        ctx_text = (r.get("content") or "")[:1000]  # batasi per dokumen max 1000 karakter
        context_parts.append(f"### {ctx_title}\n{ctx_text}\n")

    context = "\n".join(context_parts)
    if len(context) > 4000:
        context = context[:4000] + "\n...[dipotong agar muat token limit]..."


    # Optional: gunakan LLM Groq (kalau ada)
    if GROQ_CLIENT_AVAILABLE and groq_client is not None:
        try:
            prompt = f"""
You are a helpful assistant that answers questions based ONLY on the following documents.
Do NOT invent facts. If the answer is not present, state you don't know.

Documents:
{context}

Question: {question}

Answer concisely in Indonesian (max ~200 words). Start with one short sentence summarizing whether the docs include the answer.
"""
            # Using Groq chat completions (client API may differ; adapt if necessary)
            resp = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            text = resp.choices[0].message.content.strip()
            return text
        except Exception as e:
            print(f"[WARNING] Groq LLM call failed: {e}")
            # continue to fallback

    # Fallback: jika LLM tidak tersedia / error, kirim hasil mentah yg terambil
    snippets = []
    for r in retrieved:
        snippets.append(f"- {r.get('title') or r.get('id')}: { (r.get('content') or '')[:300] }")
    reply = "Tidak ada LLM aktif — berikut hasil dokumen teratas yang relevan:\n" + "\n".join(snippets)
    return reply
