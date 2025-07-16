import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
 
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // Allow access from outside the container
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
}) 