from flask import Blueprint, request, jsonify
from services.kb_service import add_doc, list_docs, delete_doc, reset_kb
from services.preprocess_service import process_text
from services.ocr_service import extract_text
from services.file_service import save_file
from utils.jwt_middleware import jwt_required
from utils.logger import log_info, log_error
from services.excel_service import parse_excel
import time


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/upload", methods=["POST", "OPTIONS"])
@jwt_required
def upload_file():
    start = time.time()
    try : 
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        category = request.form.get("category", "lainnya") 
        filepath = save_file(file)
        filename = file.filename.lower()

        # CEK APAKAH INI FILE EXCEL
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            rows = parse_excel(filepath)  # file dibaca pake Excel parser
            doc_ids = []

            for row in rows:
                # setiap row diubah jadi 1 dokumen
                konten = "\n".join(
                [f"{col}: {val}" for col, val in row.items() if val]
                )
                
                # masuk ke add_doc()
                doc_ids.append(add_doc(
                    content=konten,
                    source_file=file.filename,
                    category=category
                ))

            duration = time.time() - start
            log_info(f"[UPLOAD SUCCESS - EXCEL] {file.filename} | kategori={category} | total={len(doc_ids)} | durasi={duration:.2f}s")

            return jsonify({
                "message": f"Excel uploaded under category '{category}' successfully.",
                "category": category,
                "total_rows": len(doc_ids),
                "document_ids": doc_ids,
            }), 200      


    # OCR (ekstrak teks dari PDF/DOCX)
        raw_text = extract_text(filepath)

    # Preprocessing
        sections = process_text(raw_text)
        print(sections)

    # Simpan ke Chroma
        doc_ids = [
           add_doc(
            #    s["title"],
               s["content"],
               source_file=file.filename,
               category=category )
               for s in sections]


        duration = time.time() - start
        log_info(f"[UPLOAD SUCCESS] {file.filename} | kategori={category} | total={len(doc_ids)} | durasi={duration:.2f}s")
    
        return jsonify({
            "message": f"File uploaded under category '{category}' successfully.",
            "category": category,
            "total_sections": len(doc_ids),
            "document_ids": doc_ids,
            }),200
    
    except Exception as e:
        log_error(f"[UPLOAD FAILED] {file.filename if 'file' in locals() else 'unknown'} | error={e}")
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/list", methods=["GET" , "OPTIONS"])
@jwt_required
def list_docs_endpoint():
    docs = list_docs()
    return jsonify(docs)


@admin_bp.route("/delete/<doc_id>", methods=["DELETE" , "OPTIONS"])
@jwt_required
def delete_doc_endpoint(doc_id):
    delete_doc(doc_id)
    return jsonify({"message": f"Dokumen dengan id {doc_id} telah dihapus"})


@admin_bp.route("/reset_kb", methods=["POST", "OPTIONS"])
@jwt_required
def reset_kb_endpoint():
    reset_kb()
    return jsonify({"message": "Seluruh knowledge base telah dihapus"})