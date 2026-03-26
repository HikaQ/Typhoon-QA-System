<template>
  <div class="setting-container">
    <div class="setting-header">
      <h1>系统设置</h1>
      <button class="back-btn" @click="backToChat">
        ← 返回聊天
      </button>
    </div>

    <div class="settings-grid">
      <!-- 基本设置 -->
      <section class="setting-section">
        <h2>基本设置</h2>
        <div class="setting-item">
          <label>系统名称</label>
          <input v-model="settings.systemName" type="text" />
        </div>
        <div class="setting-item">
          <label>系统描述</label>
          <textarea v-model="settings.description"></textarea>
        </div>
      </section>

      <!-- API 设置 -->
      <section class="setting-section">
        <h2>API 设置</h2>
        <div class="setting-item">
          <label>LLM API 地址</label>
          <input v-model="settings.llmApiUrl" type="text" placeholder="http://api.example.com" />
        </div>
        <div class="setting-item">
          <label>API Key</label>
          <input v-model="settings.apiKey" type="password" />
        </div>
        <div class="setting-item">
          <label>模型名称</label>
          <input v-model="settings.modelName" type="text" />
        </div>
      </section>

      <!-- 数据库设置 -->
      <section class="setting-section">
        <h2>数据库设置</h2>
        <div class="setting-item">
          <label>Neo4j 地址</label>
          <input v-model="settings.neo4jUrl" type="text" placeholder="bolt://localhost:7687" />
        </div>
        <div class="setting-item">
          <label>Neo4j 用户名</label>
          <input v-model="settings.neo4jUsername" type="text" />
        </div>
        <div class="setting-item">
          <label>Neo4j 密码</label>
          <input v-model="settings.neo4jPassword" type="password" />
        </div>
      </section>

      <!-- 功能设置 -->
      <section class="setting-section">
        <h2>功能设置</h2>
        <div class="setting-item checkbox">
          <input v-model="settings.enableContextRetrieval" type="checkbox" />
          <label>启用知识图谱依据展示</label>
        </div>
        <div class="setting-item checkbox">
          <input v-model="settings.enableHistory" type="checkbox" />
          <label>启用对话历史保存</label>
        </div>
        <div class="setting-item">
          <label>最大消息长度</label>
          <input v-model.number="settings.maxMessageLength" type="number" />
        </div>
      </section>
    </div>

    <div class="setting-actions">
      <button class="btn btn-save" @click="saveSetting">保存设置</button>
      <button class="btn btn-reset" @click="resetSetting">重置</button>
    </div>

    <div v-if="saveMessage" :class="['message', saveMessage.type]">
      {{ saveMessage.text }}
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const settings = ref({
  systemName: "台风知识问答系统",
  description: "基于GraphRAG的台风灾害知识问答系统",
  llmApiUrl: "http://localhost:5000",
  apiKey: "",
  modelName: "gpt-3.5-turbo",
  neo4jUrl: "bolt://localhost:7687",
  neo4jUsername: "neo4j",
  neo4jPassword: "",
  enableContextRetrieval: true,
  enableHistory: true,
  maxMessageLength: 2000,
});

const saveMessage = ref(null);
const originalSettings = ref(JSON.parse(JSON.stringify(settings.value)));

const saveSetting = () => {
  // 保存到 localStorage
  localStorage.setItem("systemSettings", JSON.stringify(settings.value));
  originalSettings.value = JSON.parse(JSON.stringify(settings.value));
  
  saveMessage.value = {
    type: "success",
    text: "✓ 设置已保存"
  };
  
  setTimeout(() => {
    saveMessage.value = null;
  }, 3000);
};

const resetSetting = () => {
  settings.value = JSON.parse(JSON.stringify(originalSettings.value));
  saveMessage.value = {
    type: "info",
    text: "⟳ 已重置为上次保存的设置"
  };
  
  setTimeout(() => {
    saveMessage.value = null;
  }, 3000);
};

const backToChat = () => {
  router.push("/");
};

// 页面加载时从 localStorage 读取设置
const loadSettings = () => {
  const saved = localStorage.getItem("systemSettings");
  if (saved) {
    settings.value = JSON.parse(saved);
    originalSettings.value = JSON.parse(JSON.stringify(settings.value));
  }
};

loadSettings();
</script>

<style scoped>
.setting-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.setting-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e5e7eb;
}

.setting-header h1 {
  margin: 0;
  font-size: 32px;
  color: #1f2937;
}

.back-btn {
  padding: 10px 16px;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #e5e7eb;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.setting-section {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.setting-section h2 {
  margin: 0 0 20px 0;
  font-size: 18px;
  color: #374151;
  border-bottom: 2px solid #f3f4f6;
  padding-bottom: 12px;
}

.setting-item {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.setting-item.checkbox {
  flex-direction: row;
  align-items: center;
}

.setting-item.checkbox input {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.setting-item.checkbox label {
  cursor: pointer;
  font-size: 14px;
}

.setting-item label {
  font-weight: 500;
  color: #374151;
  font-size: 14px;
}

.setting-item input:not([type="checkbox"]),
.setting-item textarea {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.2s;
}

.setting-item input:not([type="checkbox"]):focus,
.setting-item textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.setting-item textarea {
  resize: vertical;
  min-height: 80px;
}

.setting-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save {
  background: #6366f1;
  color: #fff;
}

.btn-save:hover {
  background: #4f46e5;
}

.btn-reset {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-reset:hover {
  background: #e5e7eb;
}

.message {
  margin-top: 20px;
  padding: 12px 16px;
  border-radius: 6px;
  text-align: center;
  font-weight: 500;
}

.message.success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.message.info {
  background: #dbeafe;
  color: #1e40af;
  border: 1px solid #bfdbfe;
}

@media (max-width: 768px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }

  .setting-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
