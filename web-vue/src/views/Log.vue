<template>
  <div class="page-container">
    <div class="page-header">
      <h1>📋 日志记录</h1>
      <button class="btn btn-secondary" @click="clearLogs">清空日志</button>
    </div>

    <div class="filter-bar">
      <select v-model="filterType" class="filter-select">
        <option value="">所有类型</option>
        <option value="info">信息</option>
        <option value="warning">警告</option>
        <option value="error">错误</option>
      </select>
    </div>

    <div class="logs-container">
      <div v-if="filteredLogs.length === 0" class="empty-logs">暂无日志数据</div>
      <div v-for="(log, index) in filteredLogs" :key="index" class="log-item" :class="log.type">
        <div class="log-header">
          <span class="log-type">{{ log.type.toUpperCase() }}</span>
          <span class="log-time">{{ log.time }}</span>
        </div>
        <div class="log-content">{{ log.message }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const filterType = ref("");
const logs = ref([]);
const loading = ref(false);

const mapType = (status) => {
  if (!status) return "info";
  const s = String(status).toLowerCase();
  if (s === "success" || s === "info") return "info";
  if (s === "warning") return "warning";
  if (s === "failure" || s === "error") return "error";
  return "info";
};

const loadLogs = async () => {
  loading.value = true;
  try {
    const res = await fetch(`/log?limit=200`);
    if (!res.ok) throw new Error(`请求失败: ${res.status}`);
    const data = await res.json();
    logs.value = (data.logs || []).map((l) => ({
      type: mapType(l.status),
      message: l.username ? `${l.username} — ${l.action_label || l.action}` : (l.action_label || l.action),
      time: l.create_time || "",
      raw: l,
    }));
  } catch (e) {
    console.error("加载日志失败", e);
    logs.value = [{ type: "error", message: `加载失败: ${e.message}`, time: new Date().toISOString() }];
  } finally {
    loading.value = false;
  }
};

const filteredLogs = computed(() => {
  if (!filterType.value) return logs.value;
  return logs.value.filter((log) => log.type === filterType.value);
});

const clearLogs = async () => {
  if (!confirm("确定要清空所有日志吗？")) return;
  try {
    const res = await fetch(`/log`, { method: "DELETE" });
    if (!res.ok) throw new Error(`清空失败: ${res.status}`);
    await res.json();
    logs.value = [];
  } catch (e) {
    alert(`清空日志失败: ${e.message}`);
  }
};

onMounted(() => {
  loadLogs();
});
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #e5e7eb;
}

.page-header h1 {
  margin: 0;
  font-size: 28px;
  color: #1f2937;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.filter-bar {
  display: flex;
}

.filter-select {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  background: #fff;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.logs-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 600px;
  overflow-y: auto;
}

.empty-logs {
  text-align: center;
  color: #9ca3af;
  padding: 40px;
  font-size: 14px;
}

.log-item {
  background: #fff;
  padding: 12px 16px;
  border-radius: 6px;
  border-left: 4px solid;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
}

.log-item:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.log-item.info {
  border-left-color: #3b82f6;
}

.log-item.warning {
  border-left-color: #f59e0b;
  background: #fffbeb;
}

.log-item.error {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.log-type {
  font-weight: 600;
  font-size: 12px;
}

.log-item.info .log-type {
  color: #3b82f6;
}

.log-item.warning .log-type {
  color: #f59e0b;
}

.log-item.error .log-type {
  color: #ef4444;
}

.log-time {
  font-size: 12px;
  color: #9ca3af;
}

.log-content {
  color: #374151;
  font-size: 14px;
  line-height: 1.5;
}

.logs-container::-webkit-scrollbar {
  width: 6px;
}

.logs-container::-webkit-scrollbar-track {
  background: transparent;
}

.logs-container::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.logs-container::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
