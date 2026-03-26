<template>
  <div class="admin-login-container">
    <div class="admin-login-box">
      <div class="admin-login-header">
        <h1>🔐 管理员登陆</h1>
        <p>台风知识问答系统管理平台</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="adminEmail">管理员账号</label>
          <input
            id="adminEmail"
            v-model="form.email"
            type="email"
            placeholder="请输入管理员邮箱"
            required
          />
        </div>

        <div class="form-group">
          <label for="adminPassword">管理员密码</label>
          <input
            id="adminPassword"
            v-model="form.password"
            type="password"
            placeholder="请输入管理员密码"
            required
          />
        </div>

        <div class="form-group">
          <label for="verifyCode">验证码</label>
          <div class="verify-code-input">
            <input
              id="verifyCode"
              v-model="form.verifyCode"
              type="text"
              placeholder="请输入验证码"
              maxlength="4"
              required
            />
            <button type="button" class="btn-code" @click="refreshVerifyCode">
              {{ verifyCodeDisplay }}
            </button>
          </div>
        </div>

        <div class="form-options">
          <label class="checkbox">
            <input v-model="form.rememberMe" type="checkbox" />
            记住我
          </label>
        </div>

        <button type="submit" class="btn btn-login" :disabled="loading">
          {{ loading ? "登陆中..." : "管理员登陆" }}
        </button>
      </form>

      <div class="admin-login-footer">
        <router-link to="/login" class="link">← 返回用户登陆</router-link>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>

    <div class="admin-login-bg">
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
  verifyCode: "",
  rememberMe: false,
});
const loading = ref(false);
const error = ref("");

// 验证码生成
const generateVerifyCode = () => {
  return Math.random().toString(36).substring(2, 6).toUpperCase();
};

const currentVerifyCode = ref(generateVerifyCode());
const verifyCodeDisplay = ref(currentVerifyCode.value);

const refreshVerifyCode = () => {
  currentVerifyCode.value = generateVerifyCode();
  verifyCodeDisplay.value = currentVerifyCode.value;
};

const handleLogin = async () => {
  error.value = "";
  loading.value = true;

  try {
    // 验证码检查
    if (form.value.verifyCode.toUpperCase() !== currentVerifyCode.value) {
      error.value = "验证码错误";
      refreshVerifyCode();
      return;
    }

    // 模拟登陆请求
    await new Promise((resolve) => setTimeout(resolve, 1000));

    if (!form.value.email || !form.value.password) {
      error.value = "邮箱和密码不能为空";
      return;
    }

    // 简单的管理员验证（实际应该调用后端API）
    if (!form.value.email.includes("admin")) {
      error.value = "该账号不是管理员账号";
      return;
    }

    // 保存管理员信息
    const admin = {
      id: Math.random().toString(36).substr(2, 9),
      email: form.value.email,
      name: "管理员",
      type: "admin",
      loginTime: new Date().toISOString(),
    };

    localStorage.setItem("currentUser", JSON.stringify(admin));
    localStorage.setItem("adminRemember", form.value.rememberMe);

    // 跳转到管理后台
    router.push("/admin/user");
  } catch (err) {
    error.value = "登陆失败，请稍后重试";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.admin-login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  overflow: hidden;
  position: relative;
}

.admin-login-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.shape {
  position: absolute;
  opacity: 0.05;
  border-radius: 50%;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: #fff;
  top: -100px;
  left: -100px;
  animation: float 6s ease-in-out infinite;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: #fff;
  bottom: 50px;
  right: 100px;
  animation: float 8s ease-in-out infinite 1s;
}

.shape-3 {
  width: 250px;
  height: 250px;
  background: #fff;
  bottom: -100px;
  left: 10%;
  animation: float 10s ease-in-out infinite 2s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(40px);
  }
}

.admin-login-box {
  background: #fff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 20px 80px rgba(0, 0, 0, 0.4);
  width: 100%;
  max-width: 420px;
  z-index: 10;
  position: relative;
}

.admin-login-header {
  text-align: center;
  margin-bottom: 30px;
}

.admin-login-header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  color: #1e293b;
}

.admin-login-header p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.form-group {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 6px;
  font-size: 14px;
}

.form-group input {
  padding: 12px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #1e293b;
  box-shadow: 0 0 0 3px rgba(30, 41, 59, 0.1);
}

.verify-code-input {
  display: flex;
  gap: 8px;
}

.verify-code-input input {
  flex: 1;
}

.btn-code {
  padding: 10px 12px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  cursor: pointer;
  font-family: monospace;
  font-size: 16px;
  font-weight: bold;
  color: #1e293b;
  letter-spacing: 2px;
  transition: all 0.2s;
  min-width: 100px;
}

.btn-code:hover {
  background: #e2e8f0;
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

.btn-login {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
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
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.admin-login-footer {
  text-align: center;
  font-size: 14px;
}

.link {
  color: #1e293b;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.link:hover {
  color: #64748b;
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
  .admin-login-box {
    margin: 20px;
    padding: 30px 20px;
  }

  .admin-login-header h1 {
    font-size: 24px;
  }

  .shape {
    display: none;
  }
}
</style>
