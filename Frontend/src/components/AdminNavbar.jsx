import { User, Clock , LogOut, ArrowLeft } from "lucide-react"
import { logout } from "../services/auth"
import { useNavigate , useLocation } from "react-router-dom"

export default function AdminNavbar({ title }) {
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate("/admin/login")
  }

  const goBack = () => {
    navigate("/admin/dashboard")
  }

  const showBackButton = location.pathname !== "/admin/dashboard"

  return (
    <div className="bg-white border-b border-neutral-200 px-6 py-4">
      <div className="flex items-center justify-between">

        <div className="flex items-center gap-4">
           {showBackButton && (
            <button
              onClick={goBack}
              className="p-2 rounded-lg hover:bg-neutral-100 transition"
            >
              <ArrowLeft size={20} className="text-neutral-700" />
            </button>
          )}


          <h2 className="text-2xl font-bold text-neutral-900">
            {title}
          </h2>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm text-neutral-600">
            <Clock size={16} />
            <span>{new Date().toLocaleDateString("id-ID")}</span>
          </div>

          <div className="flex items-center gap-2 px-4 py-2 bg-primary-50 rounded-lg">
            <User size={16} className="text-primary-600" />
            <span className="text-sm font-medium text-primary-600">Admin</span>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 text-red-600 hover:text-red-700 transition-colors font-medium"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </div>
    </div>
  )
}
