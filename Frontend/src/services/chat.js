import apiClient from "./api"


export const askQuestion = async (question) => {
  try {
    const response = await apiClient.post("/chat/ask", {
      question,
    })
    return { success: true, data: response.data }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.message || "Pertanyaan gagal diproses",
    }
  }
}