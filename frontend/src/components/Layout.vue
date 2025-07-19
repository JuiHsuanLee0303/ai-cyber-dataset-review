<template>
  <div class="flex h-screen bg-neutral-100 font-sans">
    <!-- Mobile overlay -->
    <div 
      v-if="isMobileMenuOpen" 
      @click="closeMobileMenu"
      class="fixed inset-0 bg-black bg-opacity-50 z-40 sm:hidden"
    ></div>

    <!-- Sidebar -->
    <aside 
      :class="[
        'fixed sm:relative z-50 h-full bg-neutral-900 text-white flex-col transition-transform duration-300 ease-in-out',
        'w-64 transform',
        isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full sm:translate-x-0'
      ]"
    >
      <div class="h-20 flex items-center justify-between ps-8 pe-4 border-b border-neutral-700">
        <div class="flex items-center text-2xl font-bold">
          <span class="text-primary-main">AI</span><span class="text-white">Review</span>
        </div>
        <!-- Mobile close button -->
        <button 
          @click="closeMobileMenu"
          class="sm:hidden text-neutral-400 hover:text-white p-2"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      
      <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <p class="text-xs text-neutral-400 uppercase tracking-wider px-4">主要功能</p>
        <router-link 
          to="/" 
          @click="closeMobileMenu"
          class="flex items-center px-4 py-2 text-neutral-300 hover:bg-neutral-700 hover:text-white rounded-md transition-colors duration-200"
        >
          <span class="mx-4">關於本系統</span>
        </router-link>
        <router-link 
          to="/dashboard" 
          @click="closeMobileMenu"
          class="flex items-center px-4 py-2 text-neutral-300 hover:bg-neutral-700 hover:text-white rounded-md transition-colors duration-200"
        >
          <span class="mx-4">儀表板</span>
        </router-link>
        <router-link 
          to="/review" 
          @click="closeMobileMenu"
          class="flex items-center px-4 py-2 text-neutral-300 hover:bg-neutral-700 hover:text-white rounded-md transition-colors duration-200"
        >
          <span class="mx-4">資料審核</span>
        </router-link>
        
        <!-- Admin Section -->
        <div v-if="state.user && state.user.role === 'admin'" class="pt-6">
          <p class="text-xs text-neutral-400 uppercase tracking-wider px-4">管理員</p>
          <router-link 
            v-for="item in adminMenu"
            :key="item.to"
            :to="item.to" 
            @click="closeMobileMenu"
            class="flex items-center px-4 py-2 mt-2 text-neutral-300 hover:bg-neutral-700 hover:text-white rounded-md transition-colors duration-200"
          >
            <span class="mx-4">{{ item.text }}</span>
          </router-link>
        </div>
      </nav>
    </aside>

    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="flex justify-between items-center p-4 bg-white border-b border-neutral-200">
        <div class="flex items-center">
          <!-- Mobile menu button -->
          <button 
            @click="openMobileMenu"
            class="sm:hidden text-neutral-600 hover:text-neutral-800 p-2 mr-2"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
          <!-- Page title for mobile -->
          <h1 class="text-lg font-semibold text-neutral-800 sm:hidden">
            {{ getPageTitle() }}
          </h1>
        </div>
        <div class="flex items-center">
          <span class="text-neutral-600 mr-4 hidden sm:block">你好, {{ state.user?.username }}</span>
          <span class="text-neutral-600 mr-4 sm:hidden">{{ state.user?.username }}</span>
          <button @click="handleLogout" class="bg-secondary-main hover:bg-secondary-dark text-white font-bold py-2 px-4 rounded transition-colors duration-200 text-sm">
            登出
          </button>
        </div>
      </header>
      <!-- Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-neutral-200 p-4 sm:p-6">
        <router-view />
      </main>
    </div>
    <ConfirmModal />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import useAuth from '../store/auth'
import ConfirmModal from './ConfirmModal.vue'

const router = useRouter()
const route = useRoute()
const { state, logout } = useAuth()

const isMobileMenuOpen = ref(false)

const adminMenu = [
  { to: '/admin/raw-data', text: '待審核資料管理' },
  { to: '/admin/data', text: '最終資料集管理' },
  { to: '/admin/legal-articles', text: '法源依據管理' },
  { to: '/admin/model-stats', text: '模型統計管理' },
  { to: '/admin/users', text: '使用者管理' },
  { to: '/admin/settings', text: '系統設定' }
]

const openMobileMenu = () => {
  isMobileMenuOpen.value = true
  document.body.style.overflow = 'hidden'
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
  document.body.style.overflow = 'auto'
}

const getPageTitle = () => {
  const routeTitles = {
    '/': '關於本系統',
    '/dashboard': '儀表板',
    '/review': '資料審核',
    ...adminMenu.reduce((acc, item) => ({ ...acc, [item.to]: item.text }), {})
  }
  return routeTitles[route.path] || 'AI Review'
}

const handleLogout = () => {
  logout()
  router.push('/login')
}

router.afterEach(() => {
  if (isMobileMenuOpen.value) {
    closeMobileMenu()
  }
})
</script>

<style scoped>
/* 確保側邊欄在手機版有正確的 z-index */
@media (max-width: 640px) {
  aside {
    z-index: 50;
  }
}

/* 平滑的過渡動畫 */
.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

.router-link-exact-active {
  @apply bg-neutral-700 text-white;
}
</style>