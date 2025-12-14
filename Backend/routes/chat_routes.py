from flask import Blueprint, request, jsonify
from services.query_service import query_index
from utils.rate_limiter import rate_limit
from utils.logger import log_info, log_error

import re
from services.count_service import CountService

count_service = CountService() 

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/ask", methods=["POST", "OPTIONS"])
# @rate_limit(max_requests=5, window_seconds=60)
def ask():
    
    try:
        data = request.get_json(force=True)
        question = data.get("question", "").strip()
        q_low = question.lower()

        if not question:
            return jsonify({
                "status": "error",
                "message": "Pertanyaan tidak boleh kosong."
            }), 400

        # log_info(f"[INFO] Query masuk: {question}")  
        
        # 1️⃣ CEK: Apakah ini pertanyaan counting?
        count_result = count_service.handle_count_query(question)
        if count_result:  
            return jsonify({
                "status": "success",
                "question": question,
                "answer": count_result["answer"],
                # "meta": count_result
            }), 200

        # 2️⃣ BUKAN COUNTING — lanjut ke RAG/LLM
        answer = query_index(question)

        return jsonify({
            "status": "success",
            "question": question,
            "answer": answer
        }), 200

    except Exception as e:
        log_error(f"[ERROR] Gagal memproses pertanyaan: {e}")
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500
