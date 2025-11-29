import apiClient from "./api"

export const login = async (username, password) => {
  try {
    const response = await apiClient.post("/auth/login", {
      username,
      password,
    })
    const token = response.data.token
    localStorage.setItem("authToken", token)
    return { success: true, token }
  } catch (error) {
    return { success: false, error: error.response?.data?.error || "Login gagal" }
  }
}

export const logout = () => {
  localStorage.removeItem("authToken")
}

export const isAuthenticated = () => {
  return !!localStorage.getItem("authToken")
}