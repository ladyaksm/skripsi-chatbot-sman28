import { Link } from "react-router-dom"
import { MessageCircle } from "lucide-react"

export default function UserHome() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center p-4">
      <div className="text-center text-white">
        <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <MessageCircle size={40} />
        </div>
        <h1 className="text-4xl font-bold mb-4">Selamat Datang</h1>
        <p className="text-primary-100 text-lg mb-8 max-w-md">
          Tanyakan apa saja tentang sekolah kami kepada chatbot cerdas kami
        </p>
        <Link to="/user/chat" className="btn-primary inline-block">
          Mulai Chat
        </Link>
      </div>
    </div>
  )
}