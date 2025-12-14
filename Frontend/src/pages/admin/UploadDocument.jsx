"use client"

import { useState } from "react"
import { Upload, AlertCircle, CheckCircle } from "lucide-react"
import AdminNavbar from "../../components/AdminNavbar"
import { uploadDocument } from "../../services/documents"

export default function UploadDocument() {
  const [file, setFile] = useState(null)
  const [category, setCategory] = useState("umum")
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState(null)

  const categories = ["Profil Sekolah", "Guru", "Ekstrakurikuler", "Prestasi","spmb", "Umum"]

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (
      selectedFile &&
      [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      ].includes(selectedFile.type)
    ) {
      setFile(selectedFile)
      setStatus(null)
    } else {
      setFile(null)
      setStatus({ type: "error", message: "Hanya file PDF, DOCX, atau Excel yang didukung" })
    }
  }

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      setStatus({ type: "error", message: "Silakan pilih file terlebih dahulu" })
      return
    }

    setLoading(true)
    const result = await uploadDocument(file, category)
    setLoading(false)

    if (result.success) {
      setStatus({ type: "success", message: `${file.name} berhasil diunggah dengan kategori "${category}"` })
      setFile(null)
      setCategory(categories)
    } else {
      setStatus({ type: "error", message: result.error })
    }
  }

  return (
    <div className="flex-1 flex flex-col">
      <AdminNavbar title="Upload Dokumen" />
      <div className="flex-1 p-6 bg-neutral-50 flex justify-center">
        <div className="w-full max-w-2xl">
          <form onSubmit={handleUpload} className="card p-8">
            <div className="mb-6">
              <label className="block text-sm font-medium text-neutral-700 mb-2">Kategori Dokumen</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="input-field"
                disabled={loading}
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat.toLowerCase()}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-neutral-700 mb-3">Pilih File</label>
              <div className="border-2 border-dashed border-neutral-300 rounded-lg p-8 text-center hover:border-primary-500 transition-colors">
                <input
                  type="file"
                  onChange={handleFileChange}
                  accept=".pdf,.docx,.xlsx"
                  className="hidden"
                  id="file-input"
                  disabled={loading}
                />
                <label htmlFor="file-input" className="cursor-pointer">
                  <Upload className="mx-auto mb-2 text-primary-600" size={32} />
                  <p className="text-neutral-600 font-medium">{file ? file.name : "Klik atau drag file ke sini"}</p>
                  <p className="text-xs text-neutral-500 mt-1">PDF, DOCX, atau Excel (Maksimal 10MB)</p>
                </label>
              </div>
            </div>

            {status && (
              <div
                className={`mb-6 p-4 rounded-lg flex items-gap-2 ${
                  status.type === "success" ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"
                }`}
              >
                {status.type === "success" ? (
                  <CheckCircle size={18} className="text-green-600 flex-shrink-0" />
                ) : (
                  <AlertCircle size={18} className="text-red-600 flex-shrink-0" />
                )}
                <p className={`text-sm ${status.type === "success" ? "text-green-600" : "text-red-600"}`}>
                  {status.message}
                </p>
              </div>
            )}

            <button
              type="submit"
              disabled={!file || loading}
              className="btn-primary w-full flex items-center justify-center gap-2"
            >
              <Upload size={18} />
              {loading ? "Sedang upload..." : "Upload Dokumen"}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}