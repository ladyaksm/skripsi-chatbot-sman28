"use client";

import { useState, useEffect } from "react";
import { RefreshCw, Trash2, AlertCircle } from "lucide-react";
import AdminNavbar from "../../components/AdminNavbar";
import { fetchDocuments, deleteDocument } from "../../services/api";

export default function DocumentList() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const result = await fetchDocuments();

      if (result.success) {
        setDocuments(result.data); // langsung array dari backend
        setError(null);
      }
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleDelete = async (id) => {
    if (!confirm("Yakin mau hapus dokumen ini?")) return;

    try {
      await deleteDocument(id);
      alert("Dokumen berhasil dihapus");
      loadDocuments(); // refresh list
    } catch (err) {
      alert("Gagal menghapus: " + err.message);
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      <AdminNavbar title="Daftar Dokumen"  />
      <div className="flex-1 p-6 bg-neutral-50">
        <div className="mb-6 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-neutral-900">
            Total Dokumen: {documents.length}
          </h3>
          <button
            onClick={loadDocuments}
            disabled={loading}
            className="btn-secondary flex items-center gap-2"
          >
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-2">
            <AlertCircle size={18} className="text-red-600" />
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        <div className="card overflow-hidden">
          {loading ? (
            <div className="p-8 text-center">
              <div className="inline-block animate-spin">
                <RefreshCw size={32} className="text-primary-600" />
              </div>
              <p className="text-neutral-600 mt-4">Memuat dokumen...</p>
            </div>
          ) : documents.length === 0 ? (
            <div className="p-8 text-center text-neutral-600">
              <p>Belum ada dokumen</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-neutral-100 border-b border-neutral-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-neutral-700">Nama</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-neutral-700">Kategori</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-neutral-700">Tanggal</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-neutral-700">Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  {documents.map((doc) => (
                    <tr key={doc.id} className="border-b hover:bg-neutral-50">
                      <td className="px-6 py-3">{doc.filename}</td>
                      <td className="px-6 py-3">{doc.category || "-"}</td>
                      <td className="px-6 py-3">
                        {new Date(doc.created_at).toLocaleDateString("id-ID")}
                      </td>
                      <td className="px-6 py-3">
                        <button
                          onClick={() => handleDelete(doc.id)}
                          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded flex items-center gap-1"
                        >
                          <Trash2 size={16} />
                          Hapus
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
