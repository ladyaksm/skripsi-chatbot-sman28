import { ArrowLeft, Trash2 } from "lucide-react"
import { Link } from "react-router-dom"

export default function ChatHistory() {
  const conversations = [
    { id: 1, title: "Informasi Guru Matematika", date: "2024-01-15", messages: 5 },
    { id: 2, title: "Ekstrakurikuler Tersedia", date: "2024-01-14", messages: 3 },
    { id: 3, title: "Prestasi Sekolah 2025", date: "2024-01-13", messages: 8 },
  ]

  return (
    <div className="min-h-screen bg-neutral-50">
      <div className="max-w-4xl mx-auto p-6">
        <Link
          to="/user/chat"
          className="flex items-center gap-2 text-primary-600 hover:text-primary-700 mb-8 font-medium"
        >
          <ArrowLeft size={20} />
          Kembali ke Chat
        </Link>

        <div className="mb-8">
          <h1 className="text-3xl font-bold text-neutral-900">Riwayat Obrolan</h1>
          <p className="text-neutral-600 mt-2">Lihat dan kelola riwayat percakapan Anda</p>
        </div>

        <div className="space-y-3">
          {conversations.map((conv) => (
            <div key={conv.id} className="card p-4 flex items-center justify-between hover:shadow-md transition-shadow">
              <div>
                <h3 className="font-semibold text-neutral-900">{conv.title}</h3>
                <p className="text-sm text-neutral-600">
                  {conv.messages} pesan • {new Date(conv.date).toLocaleDateString("id-ID")}
                </p>
              </div>
              <button className="text-red-600 hover:text-red-700 p-2">
                <Trash2 size={20} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}