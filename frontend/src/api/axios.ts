import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000",
});
//jedesmal, wenn api verwendet wird, wird die authentification durchgeführt!
api.interceptors.request.use((config) => {
  // Token aus loacalStorage holen
  const token = localStorage.getItem("token");

  // Wenn ein Token da ist, wird es an den Header geklebt
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});
