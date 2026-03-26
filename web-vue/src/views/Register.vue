<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <h1>创建账户</h1>
        <p>加入台风知识问答系统</p>
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="name">用户名</label>
          <input
            id="name"
            v-model="form.name"
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
            placeholder="请输入密码（至少8个字符）"
            required
            minlength="8"
          />
          <span class="password-hint">密码强度：{{ passwordStrength }}</span>
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

        <div class="form-group checkbox">
          <input v-model="form.agreeTerms" type="checkbox" required />
          <label>我已阅读并同意<router-link to="#" class="link">服务条款</router-link>和<router-link to="#" class="link">隐私政策</router-link></label>
        </div>

        <button type="submit" class="btn btn-register" :disabled="loading">
          {{ loading ? "注册中..." : "创建账户" }}
        </button>
      </form>

      <div class="register-footer">
        <p>
          已有账号？<router-link to="/login" class="link">立即登陆</router-link>
        </p>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-if="success" class="success-message">
        {{ success }}
      </div>
    </div>

    <div class="register-bg">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const form = ref({
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
  agreeTerms: false,
});
const loading = ref(false);
const error = ref("");
const success = ref("");

const passwordStrength = computed(() => {
  const pwd = form.value.password;
  if (!pwd) return "未设置";
  if (pwd.length < 8) return "弱";
  if (/^[a-zA-Z0-9]+$/.test(pwd)) return "中";
  if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(pwd)) return "强";
  return "中";
});

const handleRegister = async () => {
  error.value = "";
  success.value = "";

  // 验证
  if (!form.value.name || !form.value.email || !form.value.password) {
    error.value = "请填写所有必填项";
    return;
  }

  if (form.value.password !== form.value.confirmPassword) {
    error.value = "两次输入的密码不一致";
    return;
  }

  if (form.value.password.length < 8) {
    error.value = "密码长度至少8个字符";
    return;
  }

  if (!form.value.agreeTerms) {
    error.value = "请同意服务条款和隐私政策";
    return;
  }

  loading.value = true;

  try {
    // 模拟注册请求
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // 保存用户信息
    const user = {
      id: Math.random().toString(36).substr(2, 9),
      email: form.value.email,
      name: form.value.name,
      type: "user",
      registrationTime: new Date().toISOString(),
    };

    localStorage.setItem("currentUser", JSON.stringify(user));

    success.value = "注册成功！正在跳转到聊天界面...";

    setTimeout(() => {
      router.push("/");
    }, 1000);
  } catch (err) {
    error.value = "注册失败，请稍后重试";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
  position: relative;
  padding: 20px 0;
}

.register-bg {
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
  right: -50px;
  animation: float 6s ease-in-out infinite;
}

.shape-2 {
  width: 200px;
  height: 200px;
  background: #fff;
  bottom: 100px;
  left: 50px;
  animation: float 8s ease-in-out infinite 1s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  background: #fff;
  top: 20%;
  right: 5%;
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

.register-box {
  background: #fff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 420px;
  z-index: 10;
  position: relative;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  color: #667eea;
}

.register-header p {
  margin: 0;
  color: #9ca3af;
  font-size: 14px;
}

.form-group {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: flex-start;
  gap: 8px;
}

.form-group.checkbox input {
  margin-top: 4px;
  cursor: pointer;
}

.form-group.checkbox label {
  font-size: 13px;
  cursor: pointer;
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
  font-family: inherit;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group.checkbox input:focus {
  box-shadow: none;
}

.password-hint {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

.btn-register {
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
  margin-top: 8px;
}

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn-register:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-footer {
  text-align: center;
  font-size: 14px;
  color: #6b7280;
  margin-top: 20px;
}

.register-footer p {
  margin: 0;
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

.success-message {
  margin-top: 16px;
  padding: 12px 14px;
  background: #dcfce7;
  color: #166534;
  border-radius: 6px;
  font-size: 14px;
  text-align: center;
}

@media (max-width: 480px) {
  .register-box {
    margin: 20px;
    padding: 30px 20px;
  }

  .register-header h1 {
    font-size: 24px;
  }

  .shape {
    display: none;
  }
}
</style>
