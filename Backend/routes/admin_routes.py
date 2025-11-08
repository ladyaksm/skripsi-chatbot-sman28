from flask import Blueprint, request, jsonify
from services.kb_service import add_doc, list_docs, delete_doc, reset_kb
from services.preprocess_service import process_text
from services.ocr_service import extract_text
from services.file_service import save_file
from utils.jwt_middleware import jwt_required
# from services.rag_service import build_index as build_rag_index

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/upload", methods=["POST"])
@jwt_required
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filepath = save_file(file)

    # --- Tahap 1: OCR (ekstrak teks dari PDF/DOCX/TXT) ---
    raw_text = extract_text(filepath)

    # --- Tahap 2: Preprocessing (bersihkan, potong, mapping ke struktur) ---
    sections = process_text(raw_text)

    # --- Tahap 3: Simpan ke Chroma ---
    doc_ids = [add_doc(s["title"], s["content"]) for s in sections]

    return jsonify({
        "message": "File processed & added to knowledge base successfully",
        "total_sections": len(doc_ids),
        "document_ids": doc_ids
    })


# @admin_bp.route("/build_index", methods=["POST"])
# @jwt_required
# def build_index_endpoint():
#     try:
#         result = build_rag_index()
#         print("=== DEBUG RESULT ===")
#         print(type(result))
#         print(result)
#         return jsonify({
#            "status": "success",
#            "message": result
#     }), 200

#     except FileNotFoundError:
#         return jsonify({
#             "status": "error",
#             "message": "File structured.json tidak ditemukan. Pastikan sudah ada dokumen yang diunggah."
#         }), 404
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"Gagal membangun index: {str(e)}"
#         }), 500


@admin_bp.route("/list", methods=["GET"])
@jwt_required
def list_docs_endpoint():
    docs = list_docs()
    return jsonify(docs)


@admin_bp.route("/delete/<doc_id>", methods=["DELETE"])
@jwt_required
def delete_doc_endpoint(doc_id):
    delete_doc(doc_id)
    return jsonify({"message": f"Dokumen dengan id {doc_id} telah dihapus"})


@admin_bp.route("/reset_kb", methods=["POST"])
@jwt_required
def reset_kb_endpoint():
    reset_kb()
    return jsonify({"message": "Seluruh knowledge base telah dihapus"})
