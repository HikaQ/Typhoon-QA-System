import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 转发日志请求到后端 Flask（本地开发时使用）
      '/log': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path,
      },
      // 常见后端路由示例（如有更多 API，请按需添加）
      '/user': 'http://localhost:5000',
      '/conversation': 'http://localhost:5000',
      '/knowledge_graph': 'http://localhost:5000'
    }
  }
})
