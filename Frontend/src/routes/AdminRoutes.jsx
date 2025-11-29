import { Routes, Route, Navigate } from "react-router-dom"
import AdminLogin from "../pages/admin/Login"
import AdminDashboard from "../pages/admin/Dashboard"
import UploadDocument from "../pages/admin/UploadDocument"
import DocumentList from "../pages/admin/DocumentList"
import ResetKB from "../pages/admin/ResetKB"
import { isAuthenticated } from "../services/auth"

function ProtectedRoute({ children }) {
  return isAuthenticated() ? children : <Navigate to="/admin/login" replace />
}

export default function AdminRoutes() {

  return (
    <Routes>
      <Route path="/login" element={<AdminLogin />} />
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <div className="flex">
              <div className="flex-1">
                <Routes>
                  <Route path="/dashboard" element={<AdminDashboard />} />
                  <Route path="/upload" element={<UploadDocument />} />
                  <Route path="/documents" element={<DocumentList />} />
                  <Route path="/reset" element={<ResetKB />} />
                  <Route path="/" element={<Navigate to="/admin/dashboard" replace />} />
                  
                </Routes>
              </div>
            </div>
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}