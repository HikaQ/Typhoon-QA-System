<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h1>🌪️ 台风知识问答系统</h1>
        <p>GraphRAG 知识库</p>
      </div>

      <form @submit.prevent="handleLogin">
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
            placeholder="请输入密码"
            required
          />
        </div>

        <div class="form-options">
          <label class="checkbox">
            <input v-model="form.rememberMe" type="checkbox" />
            记住我
          </label>
          <a href="#" class="forgot-password">忘记密码？</a>
        </div>

        <button type="submit" class="btn btn-login" :disabled="loading">
          {{ loading ? "登陆中..." : "登陆" }}
        </button>
      </form>

      <div class="divider">或</div>

      <div class="social-login">
        <button class="btn-social" title="GitHub登陆">GitHub</button>
        <button class="btn-social" title="微信登陆">微信</button>
        <button class="btn-social" title="Google登陆">Google</button>
      </div>

      <div class="login-footer">
        <p>
          还没有账号？<router-link to="/register" class="link">立即注册</router-link>
        </p>
        <p>
          是管理员？<router-link to="/admin-login" class="link">管理员登陆</router-link>
        </p>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>

    <div class="login-bg">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const form = ref({
  email: "",
  password: "",
  rememberMe: false,
});
const loading = ref(false);
const error = ref("");

const handleLogin = async () => {
  error.value = "";
  loading.value = true;

  try {
    // 模拟登陆请求
    await new Promise((resolve) => setTimeout(resolve, 1000));

    if (!form.value.email || !form.value.password) {
      error.value = "邮箱和密码不能为空";
      return;
    }

    // 保存用户信息到 localStorage
    const user = {
      id: Math.random().toString(36).substr(2, 9),
      email: form.value.email,
      name: form.value.email.split("@")[0],
      type: "user",
      loginTime: new Date().toISOString(),
    };

    localStorage.setItem("currentUser", JSON.stringify(user));
    localStorage.setItem("userRemember", form.value.rememberMe);

    // 跳转到聊天界面
    router.push("/");
  } catch (err) {
    error.value = "登陆失败，请稍后重试";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
  position: relative;
}

.login-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.shape {
  position: absolute;
  opacity: 0.1;
  border-radius: 50%;
}

.shape-1 {
  width: 300px;
  height: 300px;
  background: #fff;
  top: -50px;
  left: -50px;
  animation: float 6s ease-in-out infinite;
}

.shape-2 {
  width: 200px;
  height: 200px;
  background: #fff;
  bottom: 100px;
  right: 50px;
  animation: float 8s ease-in-out infinite 1s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  background: #fff;
  bottom: -50px;
  left: 20%;
  animation: float 10s ease-in-out infinite 2s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(30px);
  }
}

.login-box {
  background: #fff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 400px;
  z-index: 10;
  position: relative;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  color: #667eea;
}

.login-header p {
  margin: 0;
  color: #9ca3af;
  font-size: 14px;
}

.form-group {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 500;
  color: #374151;
  margin-bottom: 6px;
  font-size: 14px;
}

.form-group input {
  padding: 12px 14px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  font-size: 14px;
}

.checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 6px;
}

.checkbox input {
  cursor: pointer;
}

.forgot-password {
  color: #667eea;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-password:hover {
  color: #5568d3;
}

.btn-login {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 16px;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.divider {
  text-align: center;
  color: #d1d5db;
  margin: 20px 0;
  position: relative;
}

.divider::before,
.divider::after {
  content: "";
  position: absolute;
  top: 50%;
  width: 35%;
  height: 1px;
  background: #e5e7eb;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.social-login {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.btn-social {
  flex: 1;
  padding: 10px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-social:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
}

.login-footer {
  text-align: center;
  font-size: 14px;
  color: #6b7280;
}

.login-footer p {
  margin: 8px 0;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.link:hover {
  color: #5568d3;
}

.error-message {
  margin-top: 16px;
  padding: 12px 14px;
  background: #fee2e2;
  color: #991b1b;
  border-radius: 6px;
  font-size: 14px;
  text-align: center;
}

@media (max-width: 480px) {
  .login-box {
    margin: 20px;
    padding: 30px 20px;
  }

  .login-header h1 {
    font-size: 24px;
  }

  .shape {
    display: none;
  }
}
</style>
