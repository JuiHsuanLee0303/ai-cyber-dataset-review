import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
 
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // Allow access from outside the container
    allowedHosts: ['initially-daring-foxhound.ngrok-free.app'],
    historyApiFallback: true, // Add this line
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      },
    },
  },
  build: {
    // 確保生產環境也能正確處理 API 請求
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'axios'],
        },
      },
    },
  },
  define: {
    // 確保環境變數在生產環境中可用
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
  },
}) 