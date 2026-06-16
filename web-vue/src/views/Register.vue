<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <h1>创建账号</h1>
        <p>加入台风知识问答系统</p>
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="请输入邮箱地址"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="请输入密码（至少8位）"
            required
            minlength="8"
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            required
          />
        </div>

        <button type="submit" class="btn btn-register" :disabled="loading">
          {{ loading ? "注册中..." : "创建账号" }}
        </button>
      </form>

      <div class="register-footer">
        <p>已有账号？<router-link to="/login" class="link">立即登录</router-link></p>
      </div>

      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { saveAuth } from "../utils/auth";

const router = useRouter();
const form = ref({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
});
const loading = ref(false);
const error = ref("");
const success = ref("");

const handleRegister = async () => {
  error.value = "";
  success.value = "";

  if (!form.value.username || !form.value.email || !form.value.password) {
    error.value = "请填写所有必填项";
    return;
  }
  if (form.value.password.length < 8) {
    error.value = "密码长度至少8位";
    return;
  }
  if (form.value.password !== form.value.confirmPassword) {
    error.value = "两次输入的密码不一致";
    return;
  }

  // 临时离线模式：直接注册登录
  const hardcodedToken = "offline-user-token-" + Date.now();
  saveAuth({
    token: hardcodedToken,
    user: {
      id: 1,
      username: form.value.username.trim(),
      email: form.value.email.trim(),
      real_name: "",
      type: "user",
    },
  });
  success.value = "注册成功，正在进入系统...";
  setTimeout(() => router.push("/"), 800);
};
</script>

<style scoped>
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-box {
  width: 100%;
  max-width: 430px;
  background: #fff;
  border-radius: 12px;
  padding: 32px 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.register-header {
  text-align: center;
  margin-bottom: 24px;
}

.register-header h1 {
  margin: 0 0 6px;
  color: #374151;
  font-size: 24px;
}

.register-header p {
  margin: 0;
  color: #6b7280;
}

.form-group {
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 6px;
  color: #374151;
  font-size: 14px;
}

.form-group input {
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 10px 12px;
  font-size: 14px;
}

.btn-register {
  width: 100%;
  border: none;
  border-radius: 6px;
  padding: 10px 12px;
  font-size: 15px;
  color: #fff;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
  margin-top: 4px;
}

.btn-register:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-footer {
  margin-top: 16px;
  text-align: center;
  color: #6b7280;
  font-size: 14px;
}

.link {
  color: #4f46e5;
  text-decoration: none;
}

.error-message,
.success-message {
  margin-top: 12px;
  padding: 10px;
  border-radius: 6px;
  text-align: center;
  font-size: 14px;
}

.error-message {
  background: #fee2e2;
  color: #991b1b;
}

.success-message {
  background: #dcfce7;
  color: #166534;
}
</style>
