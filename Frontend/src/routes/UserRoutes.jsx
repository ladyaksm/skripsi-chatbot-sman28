import { Routes, Route } from "react-router-dom"
import UserChat from "../pages/user/UserChat"
import ChatHistory from "../pages/user/ChatHistory"

export default function UserRoutes() {
  return (
    <Routes>
      <Route path="/chat" element={<UserChat />} />
      <Route path="/history" element={<ChatHistory />} />
      <Route path="/" element={<UserChat />} />
    </Routes>
  )
}