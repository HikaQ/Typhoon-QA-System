<template>
  <div class="page-container">
    <div class="page-header">
      <h1>👤 用户管理</h1>
      <button class="btn btn-primary" @click="addUser">+ 添加用户</button>
    </div>

    <div class="search-bar">
      <input v-model="searchQuery" placeholder="搜索用户..." type="text" />
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>用户ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="5" class="empty-message">暂无用户数据</td>
          </tr>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>#{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.createdAt }}</td>
            <td class="action-btns">
              <button class="btn-small btn-edit" @click="editUser(user)">编辑</button>
              <button class="btn-small btn-delete" @click="deleteUser(user.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const searchQuery = ref("");
const users = ref([
  { id: 1, name: "用户1", email: "user1@example.com", createdAt: "2024-01-01" },
  { id: 2, name: "用户2", email: "user2@example.com", createdAt: "2024-01-02" },
  { id: 3, name: "用户3", email: "user3@example.com", createdAt: "2024-01-03" },
]);

const filteredUsers = computed(() => {
  return users.value.filter(
    (user) =>
      user.name.includes(searchQuery.value) ||
      user.email.includes(searchQuery.value)
  );
});

const addUser = () => {
  alert("添加用户功能开发中...");
};

const editUser = (user) => {
  alert(`编辑用户: ${user.name}`);
};

const deleteUser = (id) => {
  if (confirm("确定要删除这个用户吗？")) {
    users.value = users.value.filter((u) => u.id !== id);
  }
};
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
  background: #667eea;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn:hover {
  background: #5568d3;
}

.btn-primary {
  background: #667eea;
}

.search-bar {
  display: flex;
}

.search-bar input {
  flex: 1;
  max-width: 400px;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}

.search-bar input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.table-container {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table thead {
  background: #f3f4f6;
  border-bottom: 2px solid #e5e7eb;
}

.table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.table td {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  color: #6b7280;
  font-size: 14px;
}

.table tbody tr:hover {
  background: #f9fafb;
}

.empty-message {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  padding: 40px 16px !important;
}

.action-btns {
  display: flex;
  gap: 8px;
}

.btn-small {
  padding: 6px 12px;
  font-size: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit {
  background: #dbeafe;
  color: #1e40af;
}

.btn-edit:hover {
  background: #bfdbfe;
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background: #fecaca;
}
</style>
