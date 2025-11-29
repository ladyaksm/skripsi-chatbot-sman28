"use client"

import { useState } from "react"
import { Menu, X, LayoutDashboard, FileUp, FileText, RotateCcw, LogOut } from "lucide-react"
import { Link, useLocation } from "react-router-dom"
import { logout } from "../services/auth"

export default function AdminSidebar() {
  const [isOpen, setIsOpen] = useState(false)
  const location = useLocation()

  const menuItems = [
    { icon: LayoutDashboard, label: "Dashboard", path: "/admin/dashboard" },
    { icon: FileUp, label: "Upload Dokumen", path: "/admin/upload" },
    { icon: FileText, label: "Daftar Dokumen", path: "/admin/documents" },
    { icon: RotateCcw, label: "Reset KB", path: "/admin/reset" },
  ]

  const handleLogout = () => {
    logout()
    window.location.href = "/admin/login"
  }

  const isActive = (path) => location.pathname === path

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="md:hidden fixed top-4 left-4 z-50 bg-primary-600 text-white p-2 rounded-lg"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <aside
        className={`fixed md:relative w-64 h-screen bg-primary-900 text-white transition-transform duration-300 z-40 
          ${isOpen ? "translate-x-0" : "-translate-x-full"} md:translate-x-0`}
      >
        <div className="p-6 border-b border-primary-700">
          <h1 className="text-2xl font-bold">Chatbot RAG</h1>
          <p className="text-sm text-primary-300">Admin Panel</p>
        </div>

        <nav className="p-4 space-y-2 flex-1">
          {menuItems.map((item) => {
            const Icon = item.icon
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive(item.path) ? "bg-secondary-300 text-neutral-900" : "text-primary-200 hover:bg-primary-800"
                }`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>

        <div className="p-4 border-t border-primary-700">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 text-primary-200 hover:bg-primary-800 rounded-lg transition-colors"
          >
            <LogOut size={20} />
            <span>Keluar</span>
          </button>
        </div>
      </aside>

      {/* Mobile overlay */}
      {isOpen && <div className="fixed inset-0 bg-black/50 z-30 md:hidden" onClick={() => setIsOpen(false)} />}
    </>
  )
}
