import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import AdminRoutes from "./routes/AdminRoutes"
import UserRoutes from "./routes/UserRoutes"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/admin/*" element={<AdminRoutes />} />
        <Route path="/user/*" element={<UserRoutes />} />
        <Route path="/" element={<Navigate to="/user/chat" replace />} />
      </Routes>
    </Router>
  )
}

export default App
