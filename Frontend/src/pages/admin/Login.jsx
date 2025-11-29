"use client"

import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { AlertCircle, LogIn } from "lucide-react"

import { login } from "../../services/auth"

export default function AdminLogin() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    const result = await login(username, password)
    if (result.success) {
      navigate("/admin/dashboard")
    } else {
      setError(result.error)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6
      bg-gradient-to-br from-primary-100 via-primary-400 to-primary-600">

      <div className="bg-white rounded-3xl shadow-xl max-w-md w-full p-10 border border-neutral-200">

        {/* LOGO SEKOLAH */}
      <div className="text-center mb-8">
           <div className="w-24 h-24 mx-auto">
              <img
                 src="../../assets/logo_sman28.png"
                 alt="NEXA 28"
                 className="w-full h-full object-contain drop-shadow-md"
               />
            </div>
          <h1 className="text-4xl font-extrabold text-neutral-900 mt-4">Admin Panel</h1>
          <p className="text-neutral-600 text-sm mt-1">
            Masuk untuk mengelola knowledge base
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-3 flex gap-2">
              <AlertCircle size={18} className="text-red-600" />
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          <div>
            <label className="text-sm font-medium text-neutral-700 mb-2 block">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="input-field"
              placeholder="Masukkan username"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-neutral-700 mb-2 block">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-field"
              placeholder="Masukkan password"
            />
          </div>

          <button
            type="submit"
            className="btn-primary w-full flex items-center justify-center gap-2 mt-2"
            disabled={loading}>
            {loading ? "Sedang masuk..." : "Masuk"}
          </button>
        </form>

      </div>
    </div>
  )
}
