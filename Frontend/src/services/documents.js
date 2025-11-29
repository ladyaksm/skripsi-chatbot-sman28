import apiClient from "./api"

export const uploadDocument = async (file, category) => {
  try {
    const formData = new FormData()
    formData.append("file", file)
    formData.append("category", category)

    const response = await apiClient.post("/admin/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: error.response?.data?.error || "Upload gagal" }
  }
}

export const getDocuments = async () => {
  try {
    const response = await apiClient.get("/admin/list")
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: error.response?.data?.error || "Gagal mengambil dokumen" }
  }
}

export const deleteDocument = async (docId) => {
  try {
    const response = await apiClient.delete(`/admin/delete/${docId}`)
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: error.response?.data?.error || "Gagal menghapus dokumen" }
  }
}

export const resetKnowledgeBase = async () => {
  try {
    const response = await apiClient.post("/admin/reset_kb")
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: error.response?.data?.error || "Gagal reset knowledge base" }
  }
}