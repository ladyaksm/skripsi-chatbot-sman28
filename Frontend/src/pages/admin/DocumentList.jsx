"use client";

import { useState, useEffect } from "react";
import { RefreshCw, Trash2, AlertCircle } from "lucide-react";
import AdminNavbar from "../../components/AdminNavbar";
import { getDocuments, deleteDocument } from "../../services/documents";

export default function DocumentList() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");
  const [filterCategory, setFilterCategory] = useState("");


  const loadDocuments = async () => {
    try {
      setLoading(true);
      const result = await getDocuments();

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

    // Ambil kategori unik (buat dropdown)
  const uniqueCategories = [...new Set(documents.map((d) => d.category))];

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

  // Filter sebelum tampil
  const filteredDocs = documents
    .filter((doc) =>
      doc.name?.toLowerCase().includes(search.toLowerCase())
    )
    .filter((doc) =>
      filterCategory ? doc.category === filterCategory : true
    );


  return (
    <div className="flex-1 flex flex-col">
      <AdminNavbar title="Daftar Dokumen"  />
      <div className="flex-1 p-6 bg-neutral-50">
          {/* HEADER */}
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

        {/* SEARCH + FILTER */}
        <div className="mb-6 flex gap-4 items-center">
          <input
            type="text"
            placeholder="Cari nama dokumen..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border border-neutral-300 rounded-lg px-3 py-2 w-64"
          />

          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="border border-neutral-300 rounded-lg px-3 py-2"
          >
            <option value="">Semua Kategori</option>
            {uniqueCategories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-2">
            <AlertCircle size={18} className="text-red-600" />
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        {/* table */}
        <div className="card overflow-hidden">
          {loading ? (
            <div className="p-8 text-center">
              <div className="inline-block animate-spin">
                <RefreshCw size={32} className="text-primary-600" />
              </div>
              <p className="text-neutral-600 mt-4">Memuat dokumen...</p>
            </div>
          ) : filteredDocs.length === 0 ? (
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
                  {filteredDocs.map((doc) => (
                    <tr key={doc.id} className="border-b hover:bg-neutral-50">
                      <td className="px-6 py-3">{doc.name || "-"}</td>
                      <td className="px-6 py-3">
                        <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-600">
                          {doc.category}
                        </span>
                      </td>

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
