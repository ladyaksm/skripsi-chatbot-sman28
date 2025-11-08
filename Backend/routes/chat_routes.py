from flask import Blueprint, request, jsonify
from services.rag_service import query_index

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(force=True)
        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "status": "error",
                "message": "Pertanyaan tidak boleh kosong."
            }), 400

        print(f"[INFO] Query masuk: {question}")  # log sederhana di server

        answer = query_index(question)

        return jsonify({
            "status": "success",
            "question": question,
            "answer": answer
        }), 200

    except Exception as e:
        print(f"[ERROR] Gagal memproses pertanyaan: {e}")
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500
