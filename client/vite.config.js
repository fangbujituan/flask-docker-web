import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:22048',
        changeOrigin: true
      }
    }
  },
  // 生产环境基础路径
  base: '/'
})
