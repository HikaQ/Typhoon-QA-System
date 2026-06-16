<template>
  <div class="profile-container">
    <div class="profile-header">
      <button class="btn-back" @click="goBack">← 返回</button>
      <h1>👤 个人中心</h1>
      <button v-if="!editing" class="btn btn-primary" @click="editMode">编辑信息</button>
      <div v-else class="button-group">
        <button class="btn btn-success" @click="saveProfile">保存</button>
        <button class="btn btn-secondary" @click="cancelEdit">取消</button>
      </div>
    </div>

    <div class="profile-content">
      <!-- 头像部分 -->
      <div class="avatar-section">
        <div class="avatar-placeholder">
          <div v-if="profileForm.avatar" class="avatar-image">
            {{ profileForm.avatar }}
          </div>
          <div v-else class="avatar-initial">
            {{ profileForm.username.charAt(0).toUpperCase() }}
          </div>
        </div>
        <div v-if="editing" class="avatar-edit">
          <input
            v-model="profileForm.avatar"
            type="text"
            placeholder="输入头像emoji或URL"
            class="input-field"
          />
        </div>
      </div>

      <!-- 基本信息卡片 -->
      <div class="profile-card">
        <h2>基本信息</h2>
        <div class="info-grid">
          <!-- 用户名 -->
          <div class="info-item">
            <label>用户名</label>
            <div v-if="!editing" class="info-value">{{ profileForm.username }}</div>
            <input
              v-else
              v-model="profileForm.username"
              type="text"
              disabled
              class="input-field disabled"
            />
          </div>

          <!-- 邮箱 -->
          <div class="info-item">
            <label>邮箱</label>
            <div v-if="!editing" class="info-value">
              {{ profileForm.email || "未设置" }}
            </div>
            <input
              v-else
              v-model="profileForm.email"
              type="email"
              placeholder="输入邮箱地址"
              class="input-field"
            />
          </div>

          <!-- 电话 -->
          <div class="info-item">
            <label>电话</label>
            <div v-if="!editing" class="info-value">
              {{ profileForm.phone || "未设置" }}
            </div>
            <input
              v-else
              v-model="profileForm.phone"
              type="tel"
              placeholder="输入电话号码"
              class="input-field"
            />
          </div>

          <!-- 真实姓名 -->
          <div class="info-item">
            <label>真实姓名</label>
            <div v-if="!editing" class="info-value">
              {{ profileForm.real_name || "未设置" }}
            </div>
            <input
              v-else
              v-model="profileForm.real_name"
              type="text"
              placeholder="输入真实姓名"
              class="input-field"
            />
          </div>

          <!-- 账户创建时间 -->
          <div class="info-item">
            <label>创建时间</label>
            <div class="info-value">{{ profileForm.created_at }}</div>
          </div>
        </div>
      </div>

      <!-- 个人简介卡片 -->
      <div class="profile-card">
        <h2>个人简介</h2>
        <div class="info-item full-width">
          <label>简介</label>
          <div v-if="!editing" class="info-value bio-display">
            {{ profileForm.bio || "还未添加个人简介" }}
          </div>
          <textarea
            v-else
            v-model="profileForm.bio"
            placeholder="输入个人简介（最多500字）"
            rows="5"
            class="textarea-field"
            maxlength="500"
          ></textarea>
          <div v-if="editing" class="char-count">
            {{ profileForm.bio ? profileForm.bio.length : 0 }}/500
          </div>
        </div>
      </div>

      <!-- 提示信息 -->
      <div v-if="message" :class="['message', message.type]">
        {{ message.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getUserProfile, updateUserProfile } from "../api/chat";

const router = useRouter();
const editing = ref(false);
const message = ref(null);

const profileForm = reactive({
  id: null,
  username: "",
  email: "",
  phone: "",
  real_name: "",
  bio: "",
  avatar: "",
  created_at: ""
});

// 原始数据备份（用于取消编辑）
const originalProfile = reactive({});

// 加载用户信息
const loadProfile = async () => {
  try {
    const currentUser = JSON.parse(localStorage.getItem("currentUser") || "null");
    if (!currentUser || !currentUser.id) {
      router.push("/login");
      return;
    }

    const response = await getUserProfile(currentUser.id);
    const data = response.data;

    // 填充表单数据
    profileForm.id = data.id;
    profileForm.username = data.username;
    profileForm.email = data.email || "";
    profileForm.phone = data.phone || "";
    profileForm.real_name = data.real_name || "";
    profileForm.bio = data.bio || "";
    profileForm.avatar = data.avatar || "";
    profileForm.created_at = data.created_at || "未知";

    // 备份原始数据
    Object.assign(originalProfile, profileForm);
  } catch (error) {
    showMessage("加载个人信息失败", "error");
  }
};

// 进入编辑模式
const editMode = () => {
  editing.value = true;
  // 备份当前数据
  Object.assign(originalProfile, profileForm);
};

// 取消编辑
const cancelEdit = () => {
  editing.value = false;
  // 恢复原始数据
  Object.assign(profileForm, originalProfile);
};

// 保存个人信息
const saveProfile = async () => {
  try {
    // 验证邮箱格式
    if (profileForm.email && !isValidEmail(profileForm.email)) {
      showMessage("邮箱格式不正确", "error");
      return;
    }

    const updateData = {
      email: profileForm.email,
      phone: profileForm.phone,
      real_name: profileForm.real_name,
      bio: profileForm.bio,
      avatar: profileForm.avatar
    };

    await updateUserProfile(profileForm.id, updateData);
    showMessage("个人信息更新成功", "success");
    editing.value = false;

    // 更新本地存储的用户信息
    const currentUser = JSON.parse(localStorage.getItem("currentUser") || "{}");
    currentUser.email = profileForm.email;
    currentUser.real_name = profileForm.real_name;
    localStorage.setItem("currentUser", JSON.stringify(currentUser));
  } catch (error) {
    showMessage(error.response?.data?.msg || "更新失败，请重试", "error");
  }
};

// 验证邮箱格式
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// 显示提示信息
const showMessage = (text, type) => {
  message.value = { text, type };
  setTimeout(() => {
    message.value = null;
  }, 3000);
};

// 返回上一页
const goBack = () => {
  router.back();
};

// 页面加载时获取用户信息
onMounted(() => {
  loadProfile();
});
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: #f5f5f5;
  min-height: 100vh;
}

.profile-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
  gap: 20px;
}

.profile-header h1 {
  margin: 0;
  color: #333;
  font-size: 28px;
  flex: 1;
}

.btn-back {
  padding: 8px 12px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 5px;
  color: #333;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-back:hover {
  background-color: #e0e0e0;
  border-color: #bbb;
}

.button-group {
  display: flex;
  gap: 10px;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 头像部分 */
.avatar-section {
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.avatar-placeholder {
  width: 120px;
  height: 120px;
  margin: 0 auto 15px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 48px;
  font-weight: bold;
  overflow: hidden;
}

.avatar-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60px;
  background: #f0f0f0;
}

.avatar-initial {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60px;
}

.avatar-edit input {
  max-width: 300px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

/* 信息卡片 */
.profile-card {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-card h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 20px;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-item label {
  font-weight: 600;
  color: #555;
  font-size: 14px;
}

.info-value {
  padding: 12px;
  background: #f9f9f9;
  border-radius: 5px;
  color: #333;
  line-height: 1.5;
  word-break: break-word;
}

.info-value.bio-display {
  min-height: 100px;
  white-space: pre-wrap;
  background: #f0f0f0;
}

.input-field,
.textarea-field {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.3s;
}

.input-field:focus,
.textarea-field:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-field.disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
  color: #999;
}

.textarea-field {
  resize: vertical;
  min-height: 100px;
}

.char-count {
  font-size: 12px;
  color: #999;
  text-align: right;
  margin-top: 5px;
}

/* 按钮样式 */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-primary:hover {
  background-color: #5568d3;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-success {
  background-color: #48bb78;
  color: white;
}

.btn-success:hover {
  background-color: #38a169;
}

.btn-secondary {
  background-color: #cbd5e0;
  color: #333;
}

.btn-secondary:hover {
  background-color: #a0aec0;
}

/* 消息提示 */
.message {
  padding: 12px 16px;
  border-radius: 5px;
  text-align: center;
  font-weight: 500;
}

.message.success {
  background-color: #c6f6d5;
  color: #22543d;
  border: 1px solid #9ae6b4;
}

.message.error {
  background-color: #fed7d7;
  color: #742a2a;
  border: 1px solid #fc8181;
}

/* 响应式设计 */
@media (max-width: 600px) {
  .profile-container {
    padding: 15px;
  }

  .profile-header {
    flex-wrap: wrap;
    align-items: center;
  }

  .profile-header h1 {
    font-size: 24px;
    flex: 1;
    min-width: 0;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .avatar-placeholder {
    width: 80px;
    height: 80px;
    font-size: 32px;
  }

  .button-group {
    width: 100%;
    gap: 10px;
  }

  .btn {
    flex: 1;
  }
}
</style>
