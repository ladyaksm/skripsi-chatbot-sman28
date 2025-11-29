"use client";

import { useState } from "react";
import { AlertCircle, RotateCcw } from "lucide-react";
import AdminNavbar from "../../components/AdminNavbar";
import { resetKnowledgeBase } from "../../services/documents";

export default function ResetKB() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [confirmed, setConfirmed] = useState(false);

  const handleReset = async () => {
    if (!confirmed) {
      setStatus({
        type: "error",
        message: "Silakan centang konfirmasi terlebih dahulu",
      });
      return;
    }

    setLoading(true);
    const result = await resetKnowledgeBase();
    setLoading(false);

    if (result.success) {
      setStatus({
        type: "success",
        message: "Knowledge base berhasil di-reset",
      });
      setConfirmed(false);
    } else {
      setStatus({ type: "error", message: result.error });
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      <AdminNavbar title="Reset Knowledge Base"  />
      <div className="flex-1 p-6 bg-neutral-50 flex justify-center">
        <div className="w-full max-w-2xl">
          <div className="card p-8 border-2 border-red-200 bg-red-50">
            <div className="flex gap-4 mb-6">
              <AlertCircle size={32} className="text-red-600 flex-shrink-0" />
              <div>
                <h3 className="text-lg font-bold text-red-900">Peringatan!</h3>
                <p className="text-red-800 text-sm mt-1">
                  Operasi ini akan menghapus SEMUA dokumen dari knowledge base.
                </p>
              </div>
            </div>

            {status && (
              <div
                className={`mb-6 p-4 rounded-lg ${
                  status.type === "success"
                    ? "bg-green-50 border border-green-200"
                    : "bg-red-50 border border-red-200"
                }`}
              >
                <p
                  className={`text-sm ${
                    status.type === "success"
                      ? "text-green-600"
                      : "text-red-600"
                  }`}
                >
                  {status.message}
                </p>
              </div>
            )}

            <div className="mb-6">
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={confirmed}
                  onChange={(e) => setConfirmed(e.target.checked)}
                  disabled={loading}
                  className="w-5 h-5 text-red-600"
                />
                <span className="text-sm text-neutral-700">
                  Saya memahami dan setuju untuk menghapus semua dokumen
                </span>
              </label>
            </div>

            <button
              onClick={handleReset}
              disabled={!confirmed || loading}
              className="w-full px-4 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-neutral-400 disabled:cursor-not-allowed transition-colors font-medium flex items-center justify-center gap-2"
            >
              <RotateCcw size={18} />
              {loading ? "Sedang reset..." : "Reset Knowledge Base"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
