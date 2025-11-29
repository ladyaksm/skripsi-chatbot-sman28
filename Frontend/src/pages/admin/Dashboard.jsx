"use client"
import { Link } from "react-router-dom"
import { useState, useEffect } from "react"
import { FileText, UploadCloud, Activity, RefreshCw  } from "lucide-react"
import AdminNavbar from "../../components/AdminNavbar"
import StatsCard from "../../components/StatsCard"
import { getDocuments } from "../../services/documents"

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    totalDocuments: 0,
    uploadedToday: 0,
    categories: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    const result = await getDocuments()
    if (result.success) {
      const docs = result.data || []
      const uniqueCategories = new Set(docs.map((d) => d.category)).size
      setStats({
        totalDocuments: docs.length,
        uploadedToday: docs.filter((d) => isToday(d.created_at)).length,
        categories: uniqueCategories,
      })
    }
    setLoading(false)
  }

  const isToday = (dateString) => {
    const date = new Date(dateString)
    const today = new Date()
    return date.toDateString() === today.toDateString()
  }

  return (
    <div className="flex-1 flex flex-col">
      <AdminNavbar title="Dashboard" />
      <div className="flex-1 p-6 bg-neutral-50">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* LIST */}
          <Link to="/admin/documents">
            <StatsCard icon={FileText} label="Kelola Dokumen" value={stats.totalDocuments} color="primary" />
          </Link>

          {/* UPLOAD */}
          <Link to="/admin/upload">
            <StatsCard icon={UploadCloud} label="Upload Dokumen" value={stats.uploadedToday} color="secondary" />
          </Link>

          {/* RESET KB */}
          <Link to="/admin/reset">
            <StatsCard icon={RefreshCw} label="Reset KB" value={stats.categories} color="neutral" />
          </Link>

        </div>

        <div className="mt-8 bg-white rounded-xl shadow-sm p-6 border border-neutral-200">
          <h3 className="text-lg font-bold text-neutral-900 mb-4">Informasi Sistem</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="p-4 bg-primary-50 rounded-lg">
              <p className="text-neutral-600">Status Backend</p>
              <p className="text-lg font-semibold text-primary-600 mt-1">Aktif</p>
            </div>
            <div className="p-4 bg-secondary-50 rounded-lg">
              <p className="text-neutral-600">Knowledge Base</p>
              <p className="text-lg font-semibold text-secondary-600 mt-1">Siap</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}