<template>
  <div class="admin-container">
    <!-- 左侧导航 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>🎛️ 管理后台</h2>
        <button class="back-to-chat" @click="backToChat" title="返回聊天">←</button>
      </div>
      <nav class="menu">
        <button
          v-for="item in menus"
          :key="item.path"
          class="menu-item"
          :class="{ active: route.path === item.path }"
          @click="go(item.path)"
        >
          <span class="menu-icon">{{ item.icon }}</span>
          <span class="menu-label">{{ item.label }}</span>
        </button>
      </nav>
      <div class="sidebar-footer">
        <button class="logout-btn" @click="logout">🚪 登出</button>
        <div class="version">v1.0.0</div>
      </div>
    </aside>

    <!-- 右侧内容 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const menus = [
  { path: "/admin/user", label: "用户管理", icon: "👤" },
  { path: "/admin/log", label: "日志记录", icon: "📋" },
  { path: "/admin/setting", label: "系统设置", icon: "⚙️" },
];

const go = (path) => {
  router.push(path);
};

const backToChat = () => {
  router.push("/");
};

const logout = () => {
  if (confirm("确定要登出吗？")) {
    localStorage.removeItem("currentUser");
    router.push("/admin-login");
  }
};
</script>

<style scoped>
.admin-container {
  display: flex;
  height: 100vh;
  background: #f9fafb;
}

/* ===== 左侧边栏 ===== */
.sidebar {
  width: 260px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  flex: 1;
}

.back-to-chat {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.back-to-chat:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateX(-2px);
}

/* 菜单 */
.menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 12px;
  gap: 8px;
  list-style: none;
  margin: 0;
}

.menu-item {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid transparent;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.2s;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(4px);
}

.menu-item.active {
  background: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.1);
}

.menu-icon {
  font-size: 18px;
  width: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-label {
  flex: 1;
  text-align: left;
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.logout-btn {
  width: 100%;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
  margin-bottom: 8px;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.version {
  font-size: 12px;
  opacity: 0.7;
}

/* ===== 右侧内容区 ===== */
.main-content {
  flex: 1;
  padding: 30px;
  background: #f9fafb;
  overflow-y: auto;
}

/* 滚动条样式 */
.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: transparent;
}

.main-content::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
