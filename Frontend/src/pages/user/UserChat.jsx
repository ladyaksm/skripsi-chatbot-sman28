"use client"

import { useState, useEffect, useRef } from "react"
import { Send, Menu, X, MessageSquare, Home, Clock } from "lucide-react"
import { Link } from "react-router-dom"
import ChatBubble from "../../components/ChatBubble"
import LoadingDots from "../../components/LoadingDots"
import { askQuestion } from "../../services/chat"

export default function UserChat() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Halo! Saya adalah chatbot yang siap membantu Anda. Tanyakan apa saja tentang sekolah kami. Apa yang ingin Anda ketahui?",
      isUser: false,
    },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage = { id: Date.now(), text: input, isUser: true }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setLoading(true)

    const result = await askQuestion(input)
    setLoading(false)

    if (result.success) {
      const botMessage = {
        id: Date.now() + 1,
        text: result.data.answer,
        isUser: false,
      }
      setMessages((prev) => [...prev, botMessage])
    } else {
      const errorMessage = {
        id: Date.now() + 1,
        text: `Maaf, terjadi kesalahan: ${result.error}`,
        isUser: false,
      }
      setMessages((prev) => [...prev, errorMessage])
    }
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-neutral-50 via-primary-50 to-secondary-50">
      {/* Sidebar */}
      <aside
        className={`w-64 bg-gradient-to-b from-primary-800 via-primary-700 to-primary-900 text-white transition-transform duration-300 flex flex-col shadow-lg
        ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} md:translate-x-0 md:relative z-40`}
      >
        {/* Header */}
        <div className="p-6 border-b border-primary-600 border-opacity-30">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-secondary-300 to-secondary-200 bg-clip-text text-transparent mb-1">
            NEXA28
          </h1>
          <p className="text-sm text-primary-200">Chatbot Das'tha</p>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-3">
          <Link
            to="/user/chat"
            className="flex items-center gap-3 px-4 py-3 rounded-xl bg-gradient-to-r from-secondary-300 to-secondary-400 text-primary-900 font-semibold hover:shadow-md transition-all"
          >
            <MessageSquare size={20} />
            <span>Chat Baru</span>
          </Link>
          
          <Link
            to="/user/history"
            className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-primary-600 hover:bg-opacity-30 transition-all"
            >
                 <Clock size={20} />
                 <span>Riwayat Chat</span>
          </Link>

        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-primary-600 border-opacity-30">
          <p className="text-xs text-primary-300 font-medium">Powered by ldyksm</p>
          <p className="text-xs text-primary-400 mt-2">Versi 1.0</p>
        </div>
      </aside>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="bg-white border-b border-neutral-100 px-6 py-4 flex items-center justify-between shadow-sm">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="md:hidden p-2 hover:bg-neutral-100 rounded-lg transition-colors text-primary-600"
          >
            {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          <div className="flex-1 text-center md:text-left md:ml-4">
            <h2 className="text-lg font-bold text-neutral-900">Chat dengan NEXA28 (Next Info Assistant 28)</h2>
            <p className="text-xs text-neutral-500">Tanya tentang informasi sekolah kami</p>
          </div>
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-600 to-primary-700 shadow-md flex items-center justify-center">
            <span className="text-white font-bold text-sm">S</span>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gradient-to-b from-neutral-50 via-primary-50 to-secondary-50">
          {messages.map((msg) => (
            <ChatBubble key={msg.id} message={msg.text} isUser={msg.isUser} />
          ))}
          {loading && (
            <div className="flex justify-start gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center flex-shrink-0 shadow-md">
                <span className="text-white text-xs font-bold">AI</span>
              </div>
              <div className="message-bot">
                <LoadingDots />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-neutral-100 p-6 shadow-lg">
          <div className="flex gap-3 max-w-4xl mx-auto">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && !loading && handleSend()}
              placeholder="Tanyakan sesuatu tentang sekolah kami..."
              className="input-field flex-1"
              disabled={loading}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send size={18} />
            </button>
          </div>
          <p className="text-xs text-neutral-400 mt-3 text-center">Tekan Enter atau klik tombol untuk mengirim</p>
        </div>
      </div>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/40 z-30 md:hidden" onClick={() => setSidebarOpen(false)} />
      )}
    </div>
  )
}
