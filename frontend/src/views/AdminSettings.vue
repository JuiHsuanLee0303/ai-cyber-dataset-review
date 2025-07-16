<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-800 mb-6">系統設定</h1>
    
    <div v-if="loading" class="text-center">載入中...</div>
    <div v-else-if="error" class="text-red-500 bg-red-100 p-4 rounded-lg">{{ error }}</div>
    
    <div v-else class="bg-white p-8 rounded-lg shadow-md max-w-2xl">
      <form @submit.prevent="saveSettings">
        
        <!-- AI Model Settings -->
        <div class="mb-8 border-b pb-8">
          <h2 class="text-xl font-semibold text-gray-700 mb-4">AI 模型設定</h2>
          
          <!-- Ollama URL -->
          <div class="mb-6">
            <label for="ollama-url" class="block text-gray-700 text-sm font-bold mb-2">
              Ollama 服務 URL
            </label>
            <div class="flex items-center space-x-2">
              <input
                type="text"
                id="ollama-url"
                v-model="form.ollama_url"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="例如: http://localhost:11434"
              />
              <button
                type="button"
                @click="testConnection"
                :disabled="isTestingConnection"
                class="px-4 py-2 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 disabled:bg-gray-400 whitespace-nowrap"
              >
                {{ isTestingConnection ? '測試中...' : '測試連線' }}
              </button>
            </div>
            <p v-if="testConnectionStatus" :class="testConnectionStatus.isError ? 'text-red-500' : 'text-green-500'" class="text-xs mt-2">
              {{ testConnectionStatus.message }}
            </p>
          </div>

          <!-- Ollama Model Selection -->
          <div class="mb-6">
            <label for="ollama-model" class="block text-gray-700 text-sm font-bold mb-2">
              Ollama 模型
            </label>
            <p class="text-xs text-gray-500 mb-2">
              從 Ollama 服務選擇一個模型用於自動再生。
            </p>
            <div class="flex items-center space-x-2">
              <select
                id="ollama-model"
                v-model="form.ollama_model"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              >
                <option v-if="ollamaModels.length === 0" value="" disabled>請先確認 URL 並刷新</option>
                <option v-for="model in ollamaModels" :key="model.name" :value="model.name">
                  {{ model.name }}
                </option>
              </select>
              <button
                type="button"
                @click="fetchOllamaModels"
                class="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 whitespace-nowrap"
              >
                刷新列表
              </button>
            </div>
          </div>

          <!-- Pull Model -->
          <div class="mb-6">
            <label for="pull-model" class="block text-gray-700 text-sm font-bold mb-2">
              下載新模型
            </label>
            <div class="flex items-center space-x-2">
              <input
                type="text"
                id="pull-model"
                v-model="modelToPull"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="例如: llama3:latest"
              />
              <button
                type="button"
                @click="pullModel"
                :disabled="isPullingModel"
                class="px-4 py-2 bg-teal-600 text-white font-semibold rounded-lg hover:bg-teal-700 disabled:bg-teal-400 whitespace-nowrap"
              >
                {{ isPullingModel ? '下載中...' : '下載' }}
              </button>
            </div>
            <div v-if="pullStatus" class="mt-2 text-sm text-gray-600 bg-gray-100 p-3 rounded">
              <pre class="whitespace-pre-wrap break-all">{{ pullStatus }}</pre>
            </div>
          </div>
        </div>

        <!-- Review Threshold -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold text-gray-700 mb-4">審核閾值設定</h2>
          
          <!-- Rejection Threshold -->
          <div class="mb-6">
            <label for="rejection-threshold" class="block text-gray-700 text-sm font-bold mb-2">
              拒絕閾值 (Rejection Threshold)
            </label>
            <p class="text-xs text-gray-500 mb-2">
              當一筆資料的拒絕數量達到此數值，將自動觸發重生成。
            </p>
            <input
              type="number"
              id="rejection-threshold"
              v-model.number="form.rejection_threshold"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              min="1"
            />
          </div>
          
          <!-- Approval Threshold -->
          <div class="mb-6">
            <label for="approval-threshold" class="block text-gray-700 text-sm font-bold mb-2">
              通過閾值 (Approval Threshold)
            </label>
            <p class="text-xs text-gray-500 mb-2">
              當一筆資料的通過數量達到此數值，將自動轉入最終資料集。
            </p>
            <input
              type="number"
              id="approval-threshold"
              v-model.number="form.approval_threshold"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              min="1"
            />
          </div>
        </div>

        <!-- Save Button -->
        <div class="mt-8 flex justify-end space-x-4">
          <button
            type="button"
            @click="testAuth"
            class="px-6 py-2 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50"
          >
            測試認證機制
          </button>
          <button
            type="submit"
            :disabled="isSaving"
            class="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:bg-blue-400"
          >
            {{ isSaving ? '儲存中...' : '儲存設定' }}
          </button>
        </div>
      </form>
      
      <div v-if="successMessage" class="mt-4 text-green-600 bg-green-100 p-3 rounded-lg text-center">
        {{ successMessage }}
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'

const { instance, refreshToken } = useAuth()
const toast = useToast()

// Page States
const loading = ref(true)
const error = ref(null)
const isSaving = ref(false)
const successMessage = ref('')

// Form and Settings
const form = ref({
  rejection_threshold: 3,
  approval_threshold: 2,
  ollama_model: '',
  ollama_url: 'http://host.docker.internal:11434'
})

// Ollama Connection and Models
const isTestingConnection = ref(false)
const testConnectionStatus = ref(null) // { isError: boolean, message: string }
const ollamaModels = ref([])
const modelToPull = ref('')
const isPullingModel = ref(false)
const pullStatus = ref('')


const fetchSettings = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await instance.get('/api/v1/settings/')
    form.value = response.data
    if (form.value.ollama_url) {
      await fetchOllamaModels()
    }
  } catch (err) {
    const errorMessage = err.response?.data?.detail || '無法載入系統設定。'
    error.value = errorMessage
    toast.error(errorMessage)
  } finally {
    loading.value = false
  }
}

const testConnection = async () => {
  isTestingConnection.value = true
  testConnectionStatus.value = null
  try {
    await instance.post('/api/v1/ollama/test', { url: form.value.ollama_url })
    testConnectionStatus.value = { isError: false, message: '連線成功！' }
    toast.success('連線成功！')
  } catch (err) {
    const errorMessage = err.response?.data?.detail || '連線失敗，請檢查 URL 或 Ollama 服務狀態。'
    testConnectionStatus.value = { isError: true, message: errorMessage }
    toast.error(errorMessage)
  } finally {
    isTestingConnection.value = false
  }
}

const fetchOllamaModels = async () => {
  if (!form.value.ollama_url) {
    toast.info('請先輸入 Ollama URL。')
    return
  }
  try {
    const response = await instance.get('/api/v1/ollama/models', { params: { url: form.value.ollama_url } })
    ollamaModels.value = response.data
    if (ollamaModels.value.length === 0) {
      toast.info('Ollama 服務中目前沒有可用的模型。')
    }
  } catch (error) {
    toast.error('無法獲取模型列表。')
    ollamaModels.value = []
  }
}

const pullModel = async () => {
  if (!modelToPull.value) {
    toast.warning('請輸入要下載的模型名稱。')
    return
  }
  isPullingModel.value = true
  pullStatus.value = `正在準備下載 ${modelToPull.value}...\n`

  try {
    const response = await instance.post('/api/v1/ollama/pull', 
      { model_name: modelToPull.value },
      { 
        responseType: 'text',
        timeout: 0 // No timeout for long-running operations
      }
    );

    // Parse the streaming response and show only important progress
    if (response.data) {
      const lines = response.data.split('\n').filter(line => line.trim())
      let hasShownDownloading = false
      
      lines.forEach(line => {
        try {
          const progressData = JSON.parse(line)
          if (progressData.status) {
            const status = progressData.status
            
            // Show important milestones
            if (status.includes('pulling manifest')) {
              pullStatus.value += `正在下載模型清單...\n`
            }
            else if (status.includes('verifying sha256 digest')) {
              pullStatus.value += `正在驗證模型完整性...\n`
            }
            else if (status.includes('writing manifest')) {
              pullStatus.value += `正在寫入模型檔案...\n`
            }
            else if (status.includes('success')) {
              pullStatus.value += `模型下載成功！\n`
            }
            else if (status.includes('error') || status.includes('failed')) {
              pullStatus.value += `錯誤: ${status}\n`
            }
            // For layer pulling, show only one message for all layers
            else if (status.includes('pulling') && status.match(/pulling ([a-f0-9]+)/)) {
              if (!hasShownDownloading) {
                pullStatus.value += `正在下載模型檔案...\n`
                hasShownDownloading = true
              }
            }
          }
        } catch(e) {
          // Ignore JSON parsing errors for incomplete lines
        }
      });
    }

    pullStatus.value += '\n下載完成！'
    toast.success(`${modelToPull.value} 模型下載完成！`)
    await fetchOllamaModels()
  } catch (err) {
    const errorMessage = err.response?.data?.detail || `下載模型失敗: ${err.message}`
    pullStatus.value += `\n錯誤: ${errorMessage}`
    toast.error(errorMessage)
  } finally {
    isPullingModel.value = false
    modelToPull.value = ''
  }
}

const saveSettings = async () => {
  isSaving.value = true
  successMessage.value = ''
  error.value = null
  try {
    await instance.put('/api/v1/settings/', { settings: form.value })
    toast.success('設定已成功儲存！')
    successMessage.value = '設定已成功儲存！'
    setTimeout(() => successMessage.value = '', 3000)
  } catch (err) {
    const errorMessage = err.response?.data?.detail || '儲存設定失敗。'
    toast.error(errorMessage)
    error.value = errorMessage
  } finally {
    isSaving.value = false
  }
}

const testAuth = async () => {
  try {
    toast.info('開始測試認證機制...')
    
    // 測試 1: 手動刷新 token
    toast.info('測試 1: 手動刷新 token')
    await refreshToken()
    toast.success('Token 刷新成功！')
    
    // 測試 2: 發送需要認證的請求
    toast.info('測試 2: 發送需要認證的請求')
    const response = await instance.get('/api/v1/auth/me')
    toast.success(`當前用戶: ${response.data.username} (${response.data.role})`)
    
    // 測試 3: 連續發送多個請求
    toast.info('測試 3: 連續發送多個請求')
    const promises = [
      instance.get('/api/v1/settings/'),
      instance.get('/api/v1/users/'),
      instance.get('/api/v1/stats/')
    ]
    await Promise.all(promises)
    toast.success('所有請求都成功完成！')
    
    toast.success('認證機制測試完成！')
  } catch (error) {
    console.error('認證測試失敗:', error)
    toast.error(`認證測試失敗: ${error.message}`)
  }
}

onMounted(fetchSettings)
</script> 