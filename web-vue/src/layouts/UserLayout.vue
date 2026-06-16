<template>
  <div class="chat-container" :class="{ 'has-modal': showProfileModal, 'sidebar-collapsed': isSidebarCollapsed, 'dark-mode': darkMode }">
    <!-- 左侧对话历史 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">{{ isSidebarCollapsed ? "T" : "TYPHOON" }}</div>
        <button class="sidebar-toggle-btn" @click="toggleSidebar">
          {{ isSidebarCollapsed ? ">" : "<" }}
        </button>
      </div>

      <div class="chat-history">
        <div
          v-for="(chat, index) in chatHistory"
          :key="index"
          class="chat-item"
          :class="{ active: currentChatIndex === index }"
          @click="selectChat(index)"
        >
          <div class="chat-item-title">{{ chat.title }}</div>
          <button class="delete-btn" @click.stop="deleteChat(index)">×</button>
        </div>
      </div>

      <div class="sidebar-footer">
        <button class="new-chat-btn" @click="newChat" title="新建对话">
          <span class="icon">+</span>
          <span v-if="!isSidebarCollapsed" class="sidebar-btn-text">新建对话</span>
        </button>
        <button class="profile-btn" @click="goToProfile" title="个人中心">
          <span class="icon">👤</span>
          <span v-if="!isSidebarCollapsed" class="sidebar-btn-text">个人中心</span>
        </button>
        <button class="theme-btn" @click="toggleDarkMode" :title="darkMode ? '浅色模式' : '深色模式'">
          <span class="icon">{{ darkMode ? '☀️' : '🌙' }}</span>
          <span v-if="!isSidebarCollapsed" class="sidebar-btn-text">{{ darkMode ? '浅色' : '深色' }}</span>
        </button>
        <button class="logout-btn" @click="logout" title="退出登录">
          <span class="icon">🚪</span>
          <span v-if="!isSidebarCollapsed" class="sidebar-btn-text">退出登录</span>
        </button>
      </div>
    </div>

    <!-- 右侧对话框 -->
    <div class="main-content">
      <div class="chat-messages">
        <div
          v-if="messages.length === 0"
          class="empty-state"
        >
          <h2>开始对话</h2>
          <p>提问关于台风的任何问题</p>
        </div>

        <div v-for="(msg, index) in messages" :key="index" class="message-group">
          <!-- 用户消息 -->
          <div v-if="msg.type === 'user'" class="message user-message">
            <div class="message-content">{{ msg.text }}</div>
          </div>

          <!-- AI -->
          <div v-if="msg.type === 'assistant'" class="message assistant-message">
            <div class="message-avatar">AI</div>
            <div class="message-body">
              <div class="message-content">{{ msg.text }}</div>
              <div v-if="msg.context" class="message-context">
                <details>
                  <summary>知识依据</summary>
                  <pre>{{ msg.context }}</pre>
                </details>
              </div>
            </div>
          </div>
        </div>

        <div v-if="loading" class="message assistant-message">
          <div class="message-avatar">AI</div>
          <div class="message-body">
            <div class="loading-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <div class="input-wrapper">
          <textarea
            v-model="question"
            placeholder="输入问题..."
            @keydown.enter.ctrl="submit"
            @keydown.enter.meta="submit"
            rows="1"
          ></textarea>
          <button 
            class="send-btn" 
            @click="submit"
            :disabled="loading || !question.trim()"
          >
            <span v-if="!loading">发送</span>
            <span v-else>...</span>
          </button>
        </div>
        <div class="input-hint">按 Ctrl+Enter 或 Cmd+Enter 发送</div>
      </div>
    </div>

    <div v-if="showProfileModal" class="profile-overlay" @click="closeProfileModal">
      <div class="profile-modal" @click.stop>
        <div class="profile-modal-header">
          <h2>个人中心</h2>
          <div class="profile-actions">
            <button v-if="!profileEditing" class="action-btn primary" @click="startEditProfile">编辑</button>
            <button v-else class="action-btn success" :disabled="profileSaving" @click="saveProfile">
              {{ profileSaving ? "保存中..." : "保存" }}
            </button>
            <button v-if="profileEditing" class="action-btn" @click="cancelEditProfile">取消</button>
            <button class="close-btn" @click="closeProfileModal">×</button>
          </div>
        </div>

        <div v-if="profileLoading" class="profile-loading">正在加载资料...</div>
        <div v-else class="profile-modal-body">
          <div class="avatar-wrap">
            <div class="avatar-circle">
              <span v-if="profileForm.avatar">{{ profileForm.avatar }}</span>
              <span v-else>{{ (profileForm.username || "?").charAt(0).toUpperCase() }}</span>
            </div>
            <input
              v-if="profileEditing"
              v-model="profileForm.avatar"
              class="profile-input"
              type="text"
              placeholder="头像 emoji 或 URL"
            />
          </div>

          <div class="profile-grid">
            <div class="profile-field">
              <label>用户名</label>
              <input class="profile-input" :value="profileForm.username" disabled />
            </div>
            <div class="profile-field">
              <label>邮箱</label>
              <input v-if="profileEditing" v-model="profileForm.email" class="profile-input" type="email" placeholder="请输入邮箱" />
              <div v-else class="profile-value">{{ profileForm.email || "未设置" }}</div>
            </div>
            <div class="profile-field">
              <label>电话</label>
              <input v-if="profileEditing" v-model="profileForm.phone" class="profile-input" type="text" placeholder="请输入电话" />
              <div v-else class="profile-value">{{ profileForm.phone || "未设置" }}</div>
            </div>
            <div class="profile-field">
              <label>真实姓名</label>
              <input v-if="profileEditing" v-model="profileForm.real_name" class="profile-input" type="text" placeholder="请输入真实姓名" />
              <div v-else class="profile-value">{{ profileForm.real_name || "未设置" }}</div>
            </div>
            <div class="profile-field profile-field-full">
              <label>个人简介</label>
              <textarea
                v-if="profileEditing"
                v-model="profileForm.bio"
                class="profile-textarea"
                rows="4"
                maxlength="500"
                placeholder="请输入个人简介"
              ></textarea>
              <div v-else class="profile-value profile-bio">{{ profileForm.bio || "还没有填写个人简介" }}</div>
            </div>
          </div>
        </div>

        <div v-if="profileMessage" :class="['profile-tip', profileMessage.type]">{{ profileMessage.text }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { askQuestion, getUserProfile, updateUserProfile } from "../api/chat";
import { clearAuth } from "../utils/auth";

const router = useRouter();

const question = ref("");
const loading = ref(false);
const currentChatIndex = ref(0);
const isSidebarCollapsed = ref(false);
const darkMode = ref(false);
const showProfileModal = ref(false);
const profileLoading = ref(false);
const profileSaving = ref(false);
const profileEditing = ref(false);
const profileMessage = ref(null);

const profileForm = reactive({
  id: null,
  username: "",
  email: "",
  phone: "",
  real_name: "",
  bio: "",
  avatar: "",
});
const profileSnapshot = reactive({});

// 对话历史和消息
const chatHistory = ref([
  { title: "台风知识问答", messages: [] }
]);

const messages = computed(() => chatHistory.value[currentChatIndex.value]?.messages || []);

// 提交问题
const submit = async () => {
  if (!question.value.trim() || loading.value) return;

  const userQuestion = question.value;
  question.value = "";

  // 添加用户消息
  messages.value.push({
    type: "user",
    text: userQuestion
  });

  loading.value = true;

  try {
    const res = await askQuestion(userQuestion);
    
    // 添加AI回复
    messages.value.push({
      type: "assistant",
      text: res.data.answer,
      context: res.data.context
    });

    if (messages.value.length === 2) {
      chatHistory.value[currentChatIndex.value].title = userQuestion.substring(0, 30) + (userQuestion.length > 30 ? "..." : "");
    }
  } catch (error) {
    messages.value.push({
      type: "assistant",
      text: "抱歉，请求失败，请重试。",
      context: error.message
    });
  }

  loading.value = false;
};

// 新建对话
const newChat = () => {
  chatHistory.value.push({
    title: "新对话",
    messages: []
  });
  currentChatIndex.value = chatHistory.value.length - 1;
};

// 选择对话
const selectChat = (index) => {
  currentChatIndex.value = index;
};

// 删除对话
const deleteChat = (index) => {
  if (chatHistory.value.length > 1) {
    chatHistory.value.splice(index, 1);
    if (currentChatIndex.value >= chatHistory.value.length) {
      currentChatIndex.value = chatHistory.value.length - 1;
    }
  }
};

// 跳转到个人中心
const showProfileTip = (text, type = "error") => {
  profileMessage.value = { text, type };
  setTimeout(() => {
    profileMessage.value = null;
  }, 2500);
};

const loadProfile = async () => {
  const currentUser = JSON.parse(localStorage.getItem("currentUser") || "null");
  if (!currentUser || !currentUser.id) {
    router.push("/login");
    return;
  }

  profileLoading.value = true;
  try {
    const response = await getUserProfile(currentUser.id);
    const data = response.data || {};
    profileForm.id = data.id;
    profileForm.username = data.username || "";
    profileForm.email = data.email || "";
    profileForm.phone = data.phone || "";
    profileForm.real_name = data.real_name || "";
    profileForm.bio = data.bio || "";
    profileForm.avatar = data.avatar || "";
    Object.assign(profileSnapshot, profileForm);
  } catch (error) {
    showProfileTip(error.response?.data?.msg || "加载个人资料失败");
  } finally {
    profileLoading.value = false;
  }
};

const goToProfile = async () => {
  showProfileModal.value = true;
  profileEditing.value = false;
  await loadProfile();
};

const closeProfileModal = () => {
  showProfileModal.value = false;
  profileEditing.value = false;
  profileMessage.value = null;
};

const startEditProfile = () => {
  profileEditing.value = true;
  Object.assign(profileSnapshot, profileForm);
};

const cancelEditProfile = () => {
  profileEditing.value = false;
  Object.assign(profileForm, profileSnapshot);
};

const saveProfile = async () => {
  if (!profileForm.id) return;
  profileSaving.value = true;
  try {
    await updateUserProfile(profileForm.id, {
      email: profileForm.email,
      phone: profileForm.phone,
      real_name: profileForm.real_name,
      bio: profileForm.bio,
      avatar: profileForm.avatar,
    });
    profileEditing.value = false;
    Object.assign(profileSnapshot, profileForm);

    const currentUser = JSON.parse(localStorage.getItem("currentUser") || "{}");
    currentUser.email = profileForm.email;
    currentUser.real_name = profileForm.real_name;
    localStorage.setItem("currentUser", JSON.stringify(currentUser));

    showProfileTip("保存成功", "success");
  } catch (error) {
    showProfileTip(error.response?.data?.msg || "保存失败");
  } finally {
    profileSaving.value = false;
  }
};


// 退出登录
const logout = () => {
  if (confirm("确定要退出登录吗？")) {
    clearAuth();
    router.push("/login");
  }
};

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value;
  localStorage.setItem('darkMode', darkMode.value ? 'true' : 'false');
};

watch(showProfileModal, (visible) => {
  document.body.style.overflow = visible ? "hidden" : "";
});

onMounted(() => {
  const savedDarkMode = localStorage.getItem('darkMode');
  if (savedDarkMode === 'true') {
    darkMode.value = true;
  }
});
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  background: #fff;
}

.chat-container.sidebar-collapsed .sidebar {
  width: 56px;
}

.chat-container.sidebar-collapsed .sidebar-logo {
  display: none;
}

.chat-container.sidebar-collapsed .chat-history {
  display: none;
}

/* ===== 深色模式 ===== */
.chat-container.dark-mode {
  background: #1a1a1a;
  color: #e0e0e0;
}

.chat-container.dark-mode .sidebar {
  background: #2d2d2d;
  border-right-color: #404040;
}

.chat-container.dark-mode .sidebar-header {
  border-bottom-color: #404040;
}

.chat-container.dark-mode .sidebar-logo {
  color: #8b9cff;
}

.chat-container.dark-mode .chat-history {
  background: #2d2d2d;
}

.chat-container.dark-mode .chat-item {
  background: #383838;
  border-color: transparent;
  color: #e0e0e0;
}

.chat-container.dark-mode .chat-item:hover {
  background: #404040;
}

.chat-container.dark-mode .chat-item.active {
  background: #3d3d7a;
  border-color: #6366f1;
}

.chat-container.dark-mode .chat-item-title {
  color: #e0e0e0;
}

.chat-container.dark-mode .chat-item.active .chat-item-title {
  color: #a0a8ff;
}

.chat-container.dark-mode .sidebar-footer {
  border-top-color: #404040;
}

.chat-container.dark-mode .new-chat-btn,
.chat-container.dark-mode .profile-btn,
.chat-container.dark-mode .theme-btn {
  background: #383838;
  border-color: #404040;
  color: #e0e0e0;
}

.chat-container.dark-mode .new-chat-btn:hover,
.chat-container.dark-mode .profile-btn:hover,
.chat-container.dark-mode .theme-btn:hover {
  background: #404040;
  border-color: #505050;
}

.chat-container.dark-mode .profile-btn:hover {
  background: #3d3d7a;
  border-color: #6366f1;
  color: #a0a8ff;
}

.chat-container.dark-mode .logout-btn {
  background: #5c2a2a;
  border-color: #704040;
  color: #ff9999;
}

.chat-container.dark-mode .logout-btn:hover {
  background: #704040;
}

.chat-container.dark-mode .sidebar-toggle-btn {
  background: #383838;
  border-color: #404040;
  color: #e0e0e0;
}

.chat-container.dark-mode .sidebar-toggle-btn:hover {
  background: #404040;
}

.chat-container.dark-mode .main-content {
  background: #1a1a1a;
}

.chat-container.dark-mode .chat-messages {
  background: #1a1a1a;
}

.chat-container.dark-mode .empty-state {
  color: #808080;
}

.chat-container.dark-mode .empty-state h2 {
  color: #b0b0b0;
}

.chat-container.dark-mode .user-message .message-content {
  background: #5a5acd;
  color: #fff;
}

.chat-container.dark-mode .message-content {
  background: #383838;
  color: #e0e0e0;
}

.chat-container.dark-mode .input-area {
  background: #2d2d2d;
  border-top-color: #404040;
}

.chat-container.dark-mode textarea {
  background: #383838;
  border-color: #404040;
  color: #e0e0e0;
}

.chat-container.dark-mode textarea:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.chat-container.dark-mode .send-btn {
  background: #6366f1;
  color: #fff;
}

.chat-container.dark-mode .send-btn:hover:not(:disabled) {
  background: #4f46e5;
}

.chat-container.dark-mode .send-btn:disabled {
  background: #505050;
}

.chat-container.dark-mode .input-hint {
  color: #808080;
}

.chat-container.dark-mode .message-context pre {
  background: #2d2d2d;
  border-color: #404040;
  color: #b0b0b0;
}

.chat-container.dark-mode .message-context summary {
  color: #8b9cff;
}

.chat-container.dark-mode .message-context summary:hover {
  background: #303060;
}

.chat-container.dark-mode .profile-overlay {
  background: rgba(15, 23, 42, 0.6);
}

.chat-container.dark-mode .profile-modal {
  background: #2d2d2d;
  border-color: #404040;
  color: #e0e0e0;
}

.chat-container.dark-mode .profile-modal-header {
  background: rgba(45, 45, 45, 0.95);
  border-bottom-color: #404040;
}

.chat-container.dark-mode .profile-modal-header h2 {
  color: #e0e0e0;
}

.chat-container.dark-mode .action-btn,
.chat-container.dark-mode .close-btn {
  background: #383838;
  border-color: #404040;
  color: #e0e0e0;
}

.chat-container.dark-mode .action-btn.primary {
  background: #6366f1;
  border-color: #6366f1;
}

.chat-container.dark-mode .action-btn.success {
  background: #16a34a;
  border-color: #16a34a;
}

.chat-container.dark-mode .profile-input,
.chat-container.dark-mode .profile-textarea {
  background: #383838;
  border-color: #404040;
  color: #e0e0e0;
}

.chat-container.dark-mode .profile-input:disabled {
  background: #2d2d2d;
}

.chat-container.dark-mode .profile-value {
  background: #1a1a1a;
  border-color: #404040;
  color: #e0e0e0;
}

.chat-container.dark-mode .profile-field label {
  color: #b0b0b0;
}

.chat-container.dark-mode .profile-loading {
  color: #b0b0b0;
}

.chat-container.dark-mode .profile-tip.success {
  background: #2d4620;
  color: #7cfc00;
}

.chat-container.dark-mode .profile-tip.error {
  background: #4d2020;
  color: #ff7777;
}

.chat-container.dark-mode .loading-dots span {
  background: #808080;
}

.chat-container.has-modal .sidebar,
.chat-container.has-modal .main-content {
  filter: blur(3px);
}

.profile-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(15, 23, 42, 0.28);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.profile-modal {
  width: min(780px, 100%);
  max-height: 88vh;
  overflow-y: auto;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.3);
  border: 1px solid #e5e7eb;
}

.profile-modal-header {
  position: sticky;
  top: 0;
  z-index: 2;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #1f2937;
}

.profile-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-btn,
.close-btn {
  border: 1px solid #d1d5db;
  background: #fff;
  color: #374151;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 13px;
  cursor: pointer;
}

.action-btn.primary {
  background: #6366f1;
  border-color: #6366f1;
  color: #fff;
}

.action-btn.success {
  background: #16a34a;
  border-color: #16a34a;
  color: #fff;
}

.action-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.close-btn {
  font-size: 18px;
  width: 36px;
  height: 36px;
  line-height: 1;
  padding: 0;
}

.profile-loading {
  padding: 36px 20px;
  text-align: center;
  color: #6b7280;
}

.profile-modal-body {
  padding: 18px 20px 20px;
}

.avatar-wrap {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.avatar-circle {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  font-weight: 700;
  flex-shrink: 0;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.profile-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.profile-field-full {
  grid-column: 1 / -1;
}

.profile-field label {
  font-size: 13px;
  color: #4b5563;
}

.profile-input,
.profile-textarea,
.profile-value {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  color: #111827;
  background: #fff;
}

.profile-input:disabled {
  background: #f3f4f6;
}

.profile-textarea {
  min-height: 96px;
  resize: vertical;
}

.profile-value {
  background: #f9fafb;
}

.profile-bio {
  white-space: pre-wrap;
}

.profile-tip {
  margin: 0 20px 20px;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
}

.profile-tip.success {
  background: #dcfce7;
  color: #166534;
}

.profile-tip.error {
  background: #fee2e2;
  color: #991b1b;
}

/* ===== 左侧边栏 ===== */
.sidebar {
  width: 260px;
  background: #f9f9f9;
  border-right: 1px solid #d1d5db;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: width 0.2s ease;
  position: relative;
}

.sidebar-header {
  padding: 12px;
  border-bottom: 1px solid #e5e7eb;
  min-height: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-logo {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #4f46e5;
}

.new-chat-btn {
  width: 100%;
  padding: 10px 12px;
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.new-chat-btn:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.new-chat-btn .icon {
  font-size: 18px;
}

/* 对话历史列表 */
.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.chat-item {
  padding: 10px 12px;
  margin: 4px 0;
  background: #fff;
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
  overflow: hidden;
}

.chat-item:hover {
  background: #f3f4f6;
}

.chat-item.active {
  background: #e0e7ff;
  border-color: #6366f1;
}

.chat-item-title {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
  color: #374151;
}

.chat-item.active .chat-item-title {
  color: #6366f1;
  font-weight: 500;
}

.delete-btn {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.chat-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: #ef4444;
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: auto;
}

.sidebar-footer .new-chat-btn {
  margin-bottom: 0;
}



.profile-btn {
  width: 100%;
  padding: 10px 12px;
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  margin-bottom: 0;
}

.profile-btn:hover {
  background: #e0e7ff;
  border-color: #6366f1;
  color: #6366f1;
}

.theme-btn {
  width: 100%;
  padding: 10px 12px;
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  margin-bottom: 0;
}

.theme-btn:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.logout-btn {
  width: 100%;
  padding: 10px 12px;
  background: #fee2e2;
  border: 1px solid #fecaca;
  color: #991b1b;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  margin-top: 0;
}

.logout-btn:hover {
  background: #fecaca;
}

.sidebar-btn-text {
  white-space: nowrap;
}

.chat-container.sidebar-collapsed .sidebar-footer {
  padding: 8px 6px;
  gap: 6px;
}

.chat-container.sidebar-collapsed .new-chat-btn,
.chat-container.sidebar-collapsed .profile-btn,
.chat-container.sidebar-collapsed .theme-btn,
.chat-container.sidebar-collapsed .logout-btn {
  padding: 8px 0;
  min-height: 34px;
}

/* ===== 右侧主内容区 ===== */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-toggle-btn {
  border: 1px solid #d1d5db;
  background: #fff;
  color: #374151;
  border-radius: 6px;
  width: 30px;
  height: 30px;
  font-size: 14px;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  transition: all 0.2s;
}

.sidebar-toggle-btn:hover {
  background: #f3f4f6;
}

.sidebar-toggle-bottom {
  width: 100%;
  height: auto;
  min-height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #9ca3af;
}

.empty-state h2 {
  font-size: 32px;
  margin: 0 0 12px 0;
  color: #6b7280;
}

.empty-state p {
  font-size: 16px;
  margin: 0;
}

/* 消息 */
.message-group {
  display: flex;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message {
  display: flex;
  gap: 12px;
  max-width: 80%;
}

.user-message {
  justify-content: flex-end;
  align-self: flex-end;
}

.user-message .message-content {
  background: #6366f1;
  color: #fff;
  padding: 12px 16px;
  border-radius: 12px;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.assistant-message {
  justify-content: flex-start;
  align-self: flex-start;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.message-body {
  flex: 1;
}

.message-content {
  background: #f3f4f6;
  padding: 12px 16px;
  border-radius: 12px;
  word-wrap: break-word;
  white-space: pre-wrap;
  color: #1f2937;
}

.message-context {
  margin-top: 8px;
  font-size: 13px;
}

.message-context details {
  cursor: pointer;
}

.message-context summary {
  color: #6366f1;
  padding: 4px 8px;
  border-radius: 4px;
  user-select: none;
}

.message-context summary:hover {
  background: #f0f4ff;
}

.message-context pre {
  background: #f9fafb;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  max-height: 200px;
  overflow-y: auto;
  margin: 8px 0 0 0;
  font-size: 12px;
  color: #4b5563;
}

/* 加载动画 */
.loading-dots {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background: #9ca3af;
  border-radius: 50%;
  animation: bounce 1.4s infinite;
}

.loading-dots span:nth-child(1) {
  animation-delay: 0s;
}

.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% {
    opacity: 0.5;
  }
  40% {
    opacity: 1;
  }
}

/* ===== 输入区域 ===== */
.input-area {
  padding: 16px 20px;
  background: #fff;
  border-top: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.input-wrapper {
  display: flex;
  gap: 8px;
}

textarea {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  max-height: 120px;
  min-height: 44px;
  transition: border-color 0.2s;
}

textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.send-btn {
  padding: 12px 24px;
  background: #6366f1;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  background: #4f46e5;
}

.send-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

.input-hint {
  margin-top: 8px;
  font-size: 12px;
  color: #9ca3af;
  text-align: right;
}

/* ===== 滚动条 ===== */
.chat-history::-webkit-scrollbar,
.chat-messages::-webkit-scrollbar,
.message-context pre::-webkit-scrollbar {
  width: 6px;
}

.chat-history::-webkit-scrollbar-track,
.chat-messages::-webkit-scrollbar-track,
.message-context pre::-webkit-scrollbar-track {
  background: transparent;
}

.chat-history::-webkit-scrollbar-thumb,
.chat-messages::-webkit-scrollbar-thumb,
.message-context pre::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.chat-history::-webkit-scrollbar-thumb:hover,
.chat-messages::-webkit-scrollbar-thumb:hover,
.message-context pre::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .message {
    max-width: 100%;
  }

  .profile-modal {
    max-height: 92vh;
  }

  .profile-grid {
    grid-template-columns: 1fr;
  }

  .avatar-wrap {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
