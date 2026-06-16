import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
  timeout: 100000,
});

export function login(payload) {
  return api.post("/user/login", payload);
}

export function adminLogin(payload) {
  return api.post("/user/admin-login", payload);
}

export function register(payload) {
  return api.post("/user/register", payload);
}
