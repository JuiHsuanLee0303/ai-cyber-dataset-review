<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-slate-100 flex items-center justify-center p-4">
    <!-- 優雅的背景裝飾 -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-20 -right-20 w-40 h-40 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-40"></div>
      <div class="absolute -bottom-20 -left-20 w-40 h-40 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-40"></div>
      <div class="absolute top-1/2 left-1/4 w-32 h-32 bg-slate-200 rounded-full mix-blend-multiply filter blur-xl opacity-30"></div>
    </div>

    <div class="relative z-10 w-full max-w-5xl">
      <!-- 系統標題與研究背景 -->
      <div class="text-center mb-8">
        <div class="flex flex-col sm:flex-row items-center justify-center mb-4">
          <div class="w-14 h-14 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-lg flex items-center justify-center mr-0 sm:mr-4 mb-3 sm:mb-0 shadow-lg">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
          </div>
          <div class="text-center sm:text-left">
            <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold bg-gradient-to-r from-slate-800 to-slate-700 bg-clip-text text-transparent mb-1">
              AI 資安資料集審核系統
            </h1>
            <p class="text-sm text-slate-600 font-medium">
              國立臺北商業大學 人工智慧與商業應用碩士班
            </p>
          </div>
        </div>
        <div class="max-w-3xl mx-auto">
          <p class="hidden sm:block text-base text-slate-700 leading-relaxed px-4 mb-2">
            結合生成式 AI、資安專家審核與迴圈式自動再生成之協同流程平台
          </p>
          <p class="text-sm text-slate-600 leading-relaxed px-4">
            碩士論文《檢索增強生成與微調大語言模型於資安管理應用之研究》實作系統
          </p>
        </div>
      </div>

      <div class="grid lg:grid-cols-3 gap-6 lg:gap-8 items-start">

        <!-- 左側：登入表單 -->
        <div class="bg-white/90 backdrop-blur-sm border border-slate-200/60 rounded-xl shadow-lg p-6 order-1 lg:order-1 col-span-2">
          <div class="text-center mb-6">
            <div class="hidden sm:block w-12 h-12 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-lg flex items-center justify-center mx-auto mb-4 shadow-md">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
              </svg>
            </div>
            <h2 class="text-xl font-semibold text-slate-800 mb-1">系統登入</h2>
            <p class="text-sm text-slate-600">請使用您的帳號密碼登入系統</p>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <label for="username" class="block text-slate-700 text-sm font-medium mb-2">
                帳號
              </label>
              <input
                type="text"
                id="username"
                v-model="username"
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80 backdrop-blur-sm hover:bg-white"
                placeholder="請輸入您的帳號"
                required
              />
            </div>

            <div>
              <label for="password" class="block text-slate-700 text-sm font-medium mb-2">
                密碼
              </label>
              <input
                type="password"
                id="password"
                v-model="password"
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80 backdrop-blur-sm hover:bg-white"
                placeholder="請輸入您的密碼"
                required
              />
            </div>

            <div v-if="error" class="bg-red-50/80 backdrop-blur-sm border border-red-200/60 rounded-lg p-3">
              <div class="flex items-center">
                <svg class="w-4 h-4 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="text-red-700 text-sm">{{ error }}</span>
              </div>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white font-medium py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
            >
              <div class="flex items-center justify-center">
                <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ loading ? '登入中...' : '登入系統' }}
              </div>
            </button>
          </form>
        </div>
          
        <!-- 右側：系統核心功能 -->
        <div class="order-2 lg:order-1 h-full flex flex-col col-span-2 sm:col-span-1">
          <!-- 系統功能區塊 -->
          <div class="hidden sm:block bg-white/80 backdrop-blur-sm border border-slate-200/60 rounded-xl p-4 lg:p-5 shadow-lg flex-1 mb-4">
            <h3 class="text-base lg:text-lg font-semibold text-slate-800 mb-4 flex items-center">
              <svg class="w-4 lg:w-5 h-4 lg:h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              系統功能
            </h3>
            <div class="space-y-3 lg:space-y-4 text-sm text-slate-700">
              <div class="flex items-start group">
                <div class="w-2 h-2 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full mt-1.5 mr-3 flex-shrink-0 group-hover:scale-110 transition-transform"></div>
                <span class="leading-relaxed group-hover:text-slate-800 transition-colors">AI 生成指令微調資料集</span>
              </div>
              <div class="flex items-start group">
                <div class="w-2 h-2 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full mt-1.5 mr-3 flex-shrink-0 group-hover:scale-110 transition-transform"></div>
                <span class="leading-relaxed group-hover:text-slate-800 transition-colors">資安專家多重審核機制</span>
              </div>
              <div class="flex items-start group">
                <div class="w-2 h-2 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full mt-1.5 mr-3 flex-shrink-0 group-hover:scale-110 transition-transform"></div>
                <span class="leading-relaxed group-hover:text-slate-800 transition-colors">迴圈式自動再生成流程</span>
              </div>
            </div>
          </div>

          <!-- 研究作者區塊 -->
          <div class="bg-gradient-to-br from-slate-50 to-blue-50/50 border border-slate-200/60 rounded-xl p-4 lg:p-5 flex-shrink-0 shadow-md">
            <h4 class="text-sm font-semibold text-slate-800 mb-3 flex items-center">
              <svg class="w-4 h-4 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              研究作者
            </h4>
            <div class="space-y-2 text-sm text-slate-700">
              <div class="flex items-center">
                <span class="font-medium text-slate-800">李睿軒 Jui-Hsuan Lee</span>
              </div>
              <div class="flex items-center text-xs text-slate-600">
                <span class="mr-2">指導教授：</span>
                <span>徐國鈞 教授</span>
              </div>
              <div class="flex items-center text-xs text-slate-600">
                <span class="mr-2">聯絡信箱：</span>
                <span class="font-mono text-indigo-700">11365008@ntub.edu.tw</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部資訊 -->
      <div class="hidden sm:block text-center mt-8 pt-6 border-t border-slate-200">
        <p class="text-sm text-slate-600">© 2024 國立臺北商業大學 人工智慧與商業應用碩士班</p>
        <p class="text-xs text-slate-500 mt-1">碩士論文實作系統 - 李睿軒</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import useAuth from '../store/auth'

const router = useRouter()
const { login } = useAuth()

const username = ref('')
const password = ref('')
const error = ref(null)
const loading = ref(false)

const handleLogin = async () => {
  error.value = null
  loading.value = true
  try {
    const success = await login(username.value, password.value)
    if (success) {
      router.push('/')
    } else {
      error.value = '登入失敗，請確認您的帳號和密碼。'
    }
  } catch (err) {
    error.value = '發生未知錯誤，請稍後再試。'
  } finally {
    loading.value = false
  }
}

const quickLogin = async (user, pass) => {
  username.value = user
  password.value = pass
  await handleLogin()
}
</script> 