import axios from "axios"

const API_BASE_URL = "http://127.0.0.1:5001"

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// // Admin: Upload
// export const uploadDocument = async (file, category) => {
//     const formData = new FormData();
//     formData.append("file", file);
//     formData.append("category", category);

//     const res = await apiClient.post("/admin/upload", formData, {
//         headers: {
//             "Content-Type": "multipart/form-data",
//         }
//     });

//     return res.data;
// };

// // Admin: List
// export const fetchDocuments = async () => {
//   const res = await apiClient.get("/admin/list");
//   return {
//     success: true,
//     data: res.data    // backend mengirim array of document object
//   };
// };

// // Admin: Delete
// export const deleteDocument = async (id) => {
//     const res = await apiClient.delete(`/admin/delete/${id}`);
//     return res.data;
// };

// // Admin: Reset KB
// export const resetKnowledgeBase = async () => {
//     const res = await apiClient.post("/admin/reset_kb");
//     return res.data;
// };

export default apiClient