import axios from "axios";
import { clearAuth, getAuthToken } from "../utils/auth";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
  timeout: 100000,
});

api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      clearAuth();
      if (window.location.pathname !== "/login" && window.location.pathname !== "/admin-login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export function askQuestion(question) {
  return api.post("/chat/ask", {
    question: question
  });
}

// 用户个人信息相关API
export function getUserProfile(userId) {
  return api.get(`/user/profile/${userId}`);
}

export function updateUserProfile(userId, profileData) {
  return api.put(`/user/profile/${userId}`, profileData);
}
