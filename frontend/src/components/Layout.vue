<template>
  <div class="flex h-screen bg-gray-100 font-sans">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-900 text-white flex-col hidden sm:flex">
      <div class="h-20 flex items-center justify-center text-2xl font-bold border-b border-gray-700">
        <span class="text-teal-400">AI</span><span class="text-white">Review</span>
      </div>
      <nav class="flex-1 px-4 py-6 space-y-2">
        <p class="text-xs text-gray-400 uppercase tracking-wider px-4">主要功能</p>
        <router-link to="/" class="flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white rounded-md transition-colors duration-200">
          <span class="mx-4">儀表板</span>
        </router-link>
        <router-link to="/review" class="flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white rounded-md transition-colors duration-200">
          <span class="mx-4">資料審核</span>
        </router-link>
        
        <!-- Admin Section -->
        <div v-if="state.user && state.user.role === 'admin'" class="pt-6">
          <p class="text-xs text-gray-400 uppercase tracking-wider px-4">管理員</p>
          <router-link to="/admin/users" class="flex items-center px-4 py-2 mt-2 text-gray-300 hover:bg-gray-700 hover:text-white rounded-md transition-colors duration-200">
            <span class="mx-4">使用者管理</span>
          </router-link>
          <router-link to="/admin/settings" class="flex items-center px-4 py-2 mt-2 text-gray-300 hover:bg-gray-700 hover:text-white rounded-md transition-colors duration-200">
            <span class="mx-4">系統設定</span>
          </router-link>
          <router-link to="/admin/raw-data" class="flex items-center px-4 py-2 mt-2 text-gray-300 hover:bg-gray-700 hover:text-white rounded-md transition-colors duration-200">
            <span class="mx-4">待審核資料管理</span>
          </router-link>
          <router-link to="/admin/data" class="flex items-center px-4 py-2 mt-2 text-gray-300 hover:bg-gray-700 hover:text-white rounded-md transition-colors duration-200">
            <span class="mx-4">最終資料集管理</span>
          </router-link>
        </div>
      </nav>
    </aside>

    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="flex justify-between items-center p-4 bg-white border-b">
        <div class="flex items-center">
            <!-- Mobile menu button can be added here -->
        </div>
        <div class="flex items-center">
          <span class="text-gray-600 mr-4">你好, {{ state.user?.username }}</span>
          <button @click="handleLogout" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200">
            登出
          </button>
        </div>
      </header>
      <!-- Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-200 p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import useAuth from '../store/auth'

const router = useRouter()
const { state, logout } = useAuth()

const handleLogout = () => {
  logout()
  router.push('/login')
}
</script> 