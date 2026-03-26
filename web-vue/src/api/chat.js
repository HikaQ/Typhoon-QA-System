import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
  timeout: 100000,
});

export function askQuestion(question) {
  return api.post("/chat/ask", {
    question: question
  });
}
