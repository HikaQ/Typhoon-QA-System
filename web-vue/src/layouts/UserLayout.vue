<template>
  <div class="chat-container">
    <!-- 左侧对话历史 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <button class="new-chat-btn" @click="newChat">
          <span class="icon">+</span> 新建对话
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
        <button class="settings-btn" @click="goToSettings">⚙️ 设置</button>
        <button class="logout-btn" @click="logout">🚪 登出</button>
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

          <!-- AI回复 -->
          <div v-if="msg.type === 'assistant'" class="message assistant-message">
            <div class="message-avatar">🤖</div>
            <div class="message-body">
              <div class="message-content">{{ msg.text }}</div>
              <div v-if="msg.context" class="message-context">
                <details>
                  <summary>📚 知识依据</summary>
                  <pre>{{ msg.context }}</pre>
                </details>
              </div>
            </div>
          </div>
        </div>

        <div v-if="loading" class="message assistant-message">
          <div class="message-avatar">🤖</div>
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
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { askQuestion } from "../api/chat";

const router = useRouter();

const question = ref("");
const loading = ref(false);
const currentChatIndex = ref(0);

// 对话历史和消息
const chatHistory = ref([
  { title: "台风知识问答", messages: [] }
]);

const messages = computed(() => chatHistory.value[currentChatIndex.value]?.messages || []);

// 提交问题
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

    // 更新对话标题（如果是第一条消息）
    if (messages.value.length === 2) {
      chatHistory.value[currentChatIndex.value].title = userQuestion.substring(0, 30) + (userQuestion.length > 30 ? "..." : "");
    }
  } catch (error) {
    messages.value.push({
      type: "assistant",
      text: "抱歉，请求失败。请重试。",
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

// 跳转到设置
const goToSettings = () => {
  router.push("/admin/setting");
};

// 登出
const logout = () => {
  if (confirm("确定要登出吗？")) {
    localStorage.removeItem("currentUser");
    router.push("/login");
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  background: #fff;
}

/* ===== 左侧边栏 ===== */
.sidebar {
  width: 260px;
  background: #f9f9f9;
  border-right: 1px solid #d1d5db;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 12px;
  border-bottom: 1px solid #e5e7eb;
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
}

.settings-btn {
  width: 100%;
  padding: 10px 12px;
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  font-size: 14px;
  transition: all 0.2s;
}

.settings-btn:hover {
  background: #f3f4f6;
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
  transition: all 0.2s;
  margin-top: 8px;
}

.logout-btn:hover {
  background: #fecaca;
}

/* ===== 右侧主内容区 ===== */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
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
}
</style>
