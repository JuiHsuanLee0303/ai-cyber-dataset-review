<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <div class="flex items-center space-x-4">
        <h1 class="text-3xl font-bold text-gray-800">待審核資料集管理</h1>
        <!-- 輪詢狀態指示器 -->
        <div v-if="isPolling" class="flex items-center space-x-2 text-sm text-blue-600">
          <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
          <span>自動更新中...</span>
        </div>
      </div>
      <div class="flex space-x-3">
        <button @click="fetchDatasets" class="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span>刷新</span>
        </button>
        <button @click="openModal()" class="px-4 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700">
          新增資料
        </button>
        <button @click="openBatchModal()" class="px-4 py-2 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <span>批量新增</span>
        </button>
      </div>
    </div>

    <!-- Datasets Cards -->
    <div v-if="loading" class="text-center py-10">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-2 text-gray-500">載入中...</p>
    </div>
    
    <div v-else-if="datasets.length === 0" class="text-center py-10 bg-white rounded-lg shadow-md">
      <div class="text-gray-400 text-6xl mb-4">📋</div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">沒有待審核資料</h3>
      <p class="text-gray-500">目前沒有需要審核的資料集。</p>
    </div>
    
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
      <div v-for="item in datasets" :key="item.id" class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
        <!-- Header -->
        <div class="p-4 border-b border-gray-200">
          <div class="flex justify-between items-start mb-3">
            <div class="flex items-center space-x-3">
              <span class="text-sm font-medium text-gray-500">#{{ item.id }}</span>
              <!-- 重新生成中狀態 -->
              <div v-if="item.review_status === 'regenerating'" class="flex items-center space-x-2">
                <div class="animate-spin rounded-full h-3 w-3 border-b-2 border-orange-500"></div>
                <span class="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded-full">
                  重新生成中
                </span>
              </div>
              <!-- 其他狀態 -->
              <span v-else-if="item.review_status === 'pending'" class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                待審核
              </span>
              <span v-else-if="item.review_status === 'reviewing'" class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
                審核中
              </span>
              <span v-else-if="item.review_status === 'done'" class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                已完成
              </span>
              <span v-else class="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded-full">
                {{ item.review_status }}
              </span>
            </div>
            <div class="flex space-x-2">
              <button @click="openModal(item)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">
                編輯
              </button>
              <button 
                @click="handleManualRegenerate(item)" 
                :disabled="item.review_status === 'regenerating'"
                :class="[
                  item.review_status === 'regenerating' 
                    ? 'text-gray-400 cursor-not-allowed' 
                    : 'text-orange-600 hover:text-orange-900'
                ]"
                class="text-sm font-medium"
              >
                重新生成
              </button>
              <button @click="handleDelete(item.id)" class="text-red-600 hover:text-red-900 text-sm font-medium">
                刪除
              </button>
            </div>
          </div>
          
          <!-- Stats -->
          <div class="flex justify-between text-sm">
            <span class="text-green-600 font-medium">通過: {{ item.accept_count }}</span>
            <button 
              @click="showRejections(item)" 
              :class="[item.reject_count > 0 ? 'text-red-600 hover:text-red-900 font-medium' : 'text-gray-400 cursor-not-allowed']"
              :disabled="item.reject_count === 0"
            >
              拒絕: {{ item.reject_count }}
            </button>
          </div>
          
          <!-- Manual Regenerate Button -->
          <div class="mt-3 pt-3 border-t border-gray-200">
            <button 
              @click="handleManualRegenerate(item)" 
              :disabled="item.review_status === 'regenerating'"
              :class="[
                item.review_status === 'regenerating'
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-orange-50 text-orange-700 hover:bg-orange-100 border-orange-200'
              ]"
              class="w-full py-2 px-3 rounded-md border text-sm font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              <svg v-if="item.review_status === 'regenerating'" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              <span>{{ item.review_status === 'regenerating' ? '重新生成中...' : '手動重新生成' }}</span>
            </button>
          </div>
        </div>
        
        <!-- Content -->
        <div class="p-4 space-y-4">
          <!-- Instruction -->
          <div>
            <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              指令 (Instruction)
            </h4>
            <div class="bg-gray-50 rounded-md p-3">
              <p class="text-sm text-gray-800 line-clamp-3">{{ item.instruction || '無' }}</p>
            </div>
          </div>
          
          <!-- Output -->
          <div>
            <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
              輸出 (Output)
            </h4>
            <div class="bg-gray-50 rounded-md p-3">
              <p class="text-sm text-gray-800 line-clamp-4">{{ item.output || '無' }}</p>
            </div>
          </div>
          
          <!-- System Prompt (if exists) -->
          <div v-if="item.system">
            <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <span class="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
              系統提示 (System)
            </h4>
            <div class="bg-gray-50 rounded-md p-3">
              <p class="text-sm text-gray-800 line-clamp-2">{{ item.system }}</p>
            </div>
          </div>
          
          <!-- Input (if exists) -->
          <div v-if="item.input">
            <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <span class="w-2 h-2 bg-yellow-500 rounded-full mr-2"></span>
              輸入 (Input)
            </h4>
            <div class="bg-gray-50 rounded-md p-3">
              <p class="text-sm text-gray-800 line-clamp-2">{{ item.input }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
        <h3 class="text-xl font-bold mb-4">{{ editingItem ? '編輯資料' : '新增資料' }}</h3>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">系統提示 (System)</label>
            <textarea v-model="form.system" rows="2" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 font-mono text-sm"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">指令 (Instruction)</label>
            <textarea v-model="form.instruction" rows="3" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 font-mono text-sm" required></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">輸入內容 (Input)</label>
            <textarea v-model="form.input" rows="3" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 font-mono text-sm"></textarea>
          </div>
           <div>
            <label class="block text-sm font-medium text-gray-700">歷史紀錄 (History - JSON format)</label>
            <textarea v-model="form.history" rows="3" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 font-mono text-sm"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">輸出 (Output)</label>
            <textarea v-model="form.output" rows="5" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 font-mono text-sm" required></textarea>
          </div>
           <div>
            <label class="block text-sm font-medium text-gray-700">資料來源 (Source) - 每行一個</label>
            <textarea v-model="form.source" rows="2" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 font-mono text-sm"></textarea>
          </div>
          <div v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</div>
          <div class="mt-6 flex justify-end space-x-4">
            <button type="button" @click="showModal = false" class="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400">取消</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">確認</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Rejection Reasons Modal -->
    <div v-if="showRejectionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-3xl">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">查看拒絕原因 (ID: {{ selectedDataset.id }})</h3>
          <button @click="closeRejectionModal" class="text-gray-500 hover:text-gray-800">&times;</button>
        </div>
        <div v-if="rejectionLoading" class="text-center py-10">載入中...</div>
        <div v-else-if="rejectionReasons.length === 0" class="text-center py-10">沒有拒絕紀錄。</div>
        <div v-else class="max-h-96 overflow-y-auto">
          <ul>
            <li v-for="reason in rejectionReasons" :key="reason.id" class="border-b py-3">
              <p class="font-mono text-gray-800">{{ reason.comment || '沒有提供原因' }}</p>
              <div class="text-xs text-gray-500 mt-2 text-right">
                <span>審核者: {{ reason.reviewer_username }}</span> | 
                <span>時間: {{ new Date(reason.timestamp).toLocaleString() }}</span>
              </div>
            </li>
          </ul>
        </div>
        <div class="mt-6 flex justify-end">
          <button @click="closeRejectionModal" class="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400">關閉</button>
        </div>
      </div>
    </div>

    <!-- Batch Add Modal -->
    <div v-if="showBatchModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold">批量新增資料</h3>
          <button @click="closeBatchModal" class="text-gray-500 hover:text-gray-800">&times;</button>
        </div>
        
        <!-- Input Methods -->
        <div class="mb-6">
          <div class="flex space-x-4 mb-4">
            <button 
              @click="batchInputMethod = 'text'"
              :class="[batchInputMethod === 'text' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700']"
              class="px-4 py-2 rounded-lg font-medium transition-colors"
            >
              貼上 JSON 文字
            </button>
            <button 
              @click="batchInputMethod = 'file'"
              :class="[batchInputMethod === 'file' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700']"
              class="px-4 py-2 rounded-lg font-medium transition-colors"
            >
              上傳 JSON 檔案
            </button>
          </div>
          
          <!-- Text Input -->
          <div v-if="batchInputMethod === 'text'" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                JSON 格式資料 (支援多筆資料的陣列格式)
              </label>
              <textarea 
                v-model="batchJsonText" 
                rows="15" 
                class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 font-mono text-sm"
                placeholder='[
  {
    "instruction": "這個資安獎懲辦法是根據什麼法律訂出來的？",
    "input": "為什麼政府要特別訂資安獎懲規定？",
    "output": "這是根據《資通安全管理法》第15條與第19條訂定的...",
    "system": "說明本辦法與母法的法律關係。",
    "history": [],
    "source": ["公務機關所屬人員資通安全事項獎懲辦法第1條"]
  }
]'
              ></textarea>
            </div>
          </div>
          
          <!-- File Input -->
          <div v-if="batchInputMethod === 'file'" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                選擇 JSON 檔案
              </label>
              <input 
                type="file" 
                @change="handleFileUpload" 
                accept=".json"
                class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
              />
              <p class="text-sm text-gray-500 mt-1">支援 .json 檔案格式</p>
            </div>
          </div>
        </div>
        
        <!-- Preview -->
        <div v-if="batchPreview.length > 0" class="mb-6">
          <h4 class="text-lg font-semibold mb-3">預覽 ({{ batchPreview.length }} 筆資料)</h4>
          <div class="max-h-64 overflow-y-auto border border-gray-200 rounded-lg p-4 bg-gray-50">
            <div v-for="(item, index) in batchPreview" :key="index" class="mb-3 p-3 bg-white rounded border">
              <div class="text-sm">
                <div class="font-medium text-gray-800">#{{ index + 1 }}</div>
                <div class="text-gray-600 mt-1">
                  <div><strong>指令:</strong> {{ item.instruction || '無' }}</div>
                  <div><strong>輸入:</strong> {{ item.input || '無' }}</div>
                  <div><strong>輸出:</strong> {{ item.output || '無' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Error Display -->
        <div v-if="batchError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-700 text-sm">{{ batchError }}</p>
        </div>
        
        <!-- Actions -->
        <div class="flex justify-between items-center">
          <div class="flex space-x-3">
            <button 
              @click="parseBatchData" 
              :disabled="!batchJsonText && batchInputMethod === 'text'"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              解析資料
            </button>
            <button 
              @click="clearBatchData" 
              class="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
            >
              清除
            </button>
          </div>
          <div class="flex space-x-3">
            <button @click="closeBatchModal" class="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400">
              取消
            </button>
            <button 
              @click="submitBatchData" 
              :disabled="batchPreview.length === 0 || batchSubmitting"
              class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {{ batchSubmitting ? '新增中...' : `確認新增 ${batchPreview.length} 筆資料` }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'
import useConfirm from '../composables/useConfirm'

const { instance } = useAuth()
const toast = useToast()
const { confirm } = useConfirm()

const datasets = ref([])
const loading = ref(true)
const error = ref(null)
const pollingInterval = ref(null)
const isPolling = ref(false)

const getInitialForm = () => ({
  instruction: '',
  input: '',
  output: '',
  system: '',
  source: '',
  history: '[]' // Default to empty JSON array string
});

// For Add/Edit Modal
const showModal = ref(false)
const editingItem = ref(null)
const form = ref(getInitialForm());

// For Rejection Reasons Modal
const showRejectionModal = ref(false)
const rejectionLoading = ref(false)
const rejectionReasons = ref([])
const selectedDataset = ref(null)

// For Batch Add Modal
const showBatchModal = ref(false)
const batchInputMethod = ref('text') // 'text' or 'file'
const batchJsonText = ref('')
const batchPreview = ref([])
const batchError = ref('')
const batchSubmitting = ref(false)

const fetchDatasets = async () => {
  loading.value = true
  try {
    const response = await instance.get('/api/v1/datasets/')
    datasets.value = response.data
    
    // 檢查是否有正在重新生成的資料
    const hasRegenerating = datasets.value.some(dataset => dataset.review_status === 'regenerating')
    
    // 如果有重新生成中的資料且尚未開始輪詢，則開始輪詢
    if (hasRegenerating && !isPolling.value) {
      startPolling()
    }
    // 如果沒有重新生成中的資料且正在輪詢，則停止輪詢
    else if (!hasRegenerating && isPolling.value) {
      stopPolling()
    }
  } catch (err) {
    error.value = '無法獲取資料列表。'
  } finally {
    loading.value = false
  }
}

// 開始輪詢重新生成狀態
const startPolling = () => {
  if (isPolling.value) return
  
  isPolling.value = true
  console.log('開始自動更新重新生成狀態...')
  
  pollingInterval.value = setInterval(async () => {
    try {
      const response = await instance.get('/api/v1/datasets/')
      const newDatasets = response.data
      
      // 檢查是否有狀態變化
      let hasChanges = false
      const oldRegeneratingCount = datasets.value.filter(d => d.review_status === 'regenerating').length
      const newRegeneratingCount = newDatasets.filter(d => d.review_status === 'regenerating').length
      
      // 檢查重新生成數量變化
      if (oldRegeneratingCount !== newRegeneratingCount) {
        hasChanges = true
      } else {
        // 檢查個別資料狀態變化
        for (let i = 0; i < newDatasets.length; i++) {
          const newDataset = newDatasets[i]
          const oldDataset = datasets.value.find(d => d.id === newDataset.id)
          
          if (!oldDataset || oldDataset.review_status !== newDataset.review_status) {
            hasChanges = true
            break
          }
        }
      }
      
      // 如果有變化，更新資料並顯示通知
      if (hasChanges) {
        console.log('檢測到狀態變化，更新資料...')
        datasets.value = newDatasets
        
        // 如果有重新生成完成的資料，顯示通知
        if (newRegeneratingCount < oldRegeneratingCount) {
          const completedCount = oldRegeneratingCount - newRegeneratingCount
          toast.success(`${completedCount} 筆資料重新生成完成！`)
          console.log(`${completedCount} 筆資料重新生成完成`)
        }
        
        // 如果沒有重新生成中的資料，停止輪詢
        if (newRegeneratingCount === 0) {
          console.log('所有重新生成完成，停止自動更新')
          stopPolling()
        }
      }
    } catch (err) {
      console.error('輪詢更新失敗:', err)
      // 如果連續失敗，停止輪詢避免無限重試
      if (err.response?.status === 401 || err.response?.status === 403) {
        console.log('認證失敗，停止自動更新')
        stopPolling()
      }
    }
  }, 3000) // 每3秒檢查一次
}

// 停止輪詢
const stopPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
    console.log('停止自動更新')
  }
  isPolling.value = false
}

const openModal = (item = null) => {
  error.value = null
  if (item) {
    editingItem.value = item;
    // Handle source array for textarea
    const sourceAsString = Array.isArray(item.source) ? item.source.join('\n') : '';
    const historyAsString = JSON.stringify(item.history || [], null, 2);
    form.value = { ...item, source: sourceAsString, history: historyAsString };
  } else {
    editingItem.value = null;
    form.value = getInitialForm();
  }
  showModal.value = true
}

const handleSubmit = async () => {
  error.value = null;
  
  let historyPayload;
  try {
    historyPayload = JSON.parse(form.value.history);
  } catch (e) {
    error.value = "History 欄位的 JSON 格式錯誤。";
    return;
  }

  // Convert source textarea back to array
  const payload = {
    ...form.value,
    source: form.value.source.split('\n').filter(s => s.trim() !== ''),
    history: historyPayload
  };

  try {
    if (editingItem.value) {
      await instance.put(`/api/v1/datasets/${editingItem.value.id}`, payload);
    } else {
      await instance.post('/api/v1/datasets/', payload);
    }
    showModal.value = false;
    await fetchDatasets();
  } catch (err) {
    error.value = `操作失敗: ${err.response?.data?.detail || '未知錯誤'}`;
  }
}

const handleDelete = async (id) => {
  const confirmed = await confirm('刪除確認', '確定要刪除這筆資料嗎？此操作無法復原。')
  if (!confirmed) return
  
  error.value = null
  try {
    await instance.delete(`/api/v1/datasets/${id}`)
    await fetchDatasets()
    toast.success('資料已成功刪除。')
  } catch (err) {
    const errorMsg = `刪除失敗: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
  }
}

const showRejections = async (item) => {
  selectedDataset.value = item
  showRejectionModal.value = true
  rejectionLoading.value = true
  rejectionReasons.value = []
  try {
    const response = await instance.get(`/api/v1/datasets/${item.id}/rejections`)
    rejectionReasons.value = response.data
  } catch (err) {
    const errorMsg = `無法獲取拒絕原因: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
  } finally {
    rejectionLoading.value = false
  }
}

const closeRejectionModal = () => {
  showRejectionModal.value = false
  rejectionReasons.value = []
  selectedDataset.value = null
}

const handleManualRegenerate = async (item) => {
  const confirmed = await confirm(
    '手動重新生成確認', 
    `確定要手動重新生成 ID ${item.id} 的資料嗎？此操作將使用 AI 重新生成內容。`
  )
  if (!confirmed) return
  
  try {
    const response = await instance.post(`/api/v1/datasets/${item.id}/regenerate`)
    toast.success('重新生成已開始，請稍候...')
    
    // 立即更新本地狀態為重新生成中
    const datasetIndex = datasets.value.findIndex(d => d.id === item.id)
    if (datasetIndex !== -1) {
      datasets.value[datasetIndex].review_status = 'regenerating'
    }
    
    // 如果尚未開始輪詢，則開始輪詢
    if (!isPolling.value) {
      startPolling()
    }
    
    console.log('手動重新生成已啟動:', response.data)
  } catch (err) {
    const errorMsg = `手動重新生成失敗: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
    console.error('手動重新生成失敗:', err)
  }
}

// Batch Add Functions
const openBatchModal = () => {
  showBatchModal.value = true
  batchError.value = ''
  batchPreview.value = []
  batchJsonText.value = ''
}

const closeBatchModal = () => {
  showBatchModal.value = false
  batchError.value = ''
  batchPreview.value = []
  batchJsonText.value = ''
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  if (file.type !== 'application/json' && !file.name.endsWith('.json')) {
    batchError.value = '請選擇有效的 JSON 檔案'
    return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      batchJsonText.value = e.target.result
      parseBatchData()
    } catch (err) {
      batchError.value = '檔案讀取失敗'
    }
  }
  reader.readAsText(file)
}

const parseBatchData = () => {
  batchError.value = ''
  batchPreview.value = []
  
  if (!batchJsonText.value.trim()) {
    batchError.value = '請輸入 JSON 資料'
    return
  }
  
  try {
    const data = JSON.parse(batchJsonText.value)
    
    if (!Array.isArray(data)) {
      batchError.value = 'JSON 資料必須是陣列格式'
      return
    }
    
    if (data.length === 0) {
      batchError.value = '陣列不能為空'
      return
    }
    
    // Validate each item
    const validData = []
    for (let i = 0; i < data.length; i++) {
      const item = data[i]
      
      if (!item.output) {
        batchError.value = `第 ${i + 1} 筆資料缺少必要的 "output" 欄位`
        return
      }
      
      // Normalize the data
      const normalizedItem = {
        instruction: item.instruction || '',
        input: item.input || '',
        output: item.output,
        system: item.system || '',
        history: Array.isArray(item.history) ? item.history : [],
        source: Array.isArray(item.source) ? item.source : []
      }
      
      validData.push(normalizedItem)
    }
    
    batchPreview.value = validData
    console.log(`成功解析 ${validData.length} 筆資料`)
    
  } catch (err) {
    batchError.value = `JSON 格式錯誤: ${err.message}`
    console.error('JSON 解析錯誤:', err)
  }
}

const clearBatchData = () => {
  batchJsonText.value = ''
  batchPreview.value = []
  batchError.value = ''
}

const submitBatchData = async () => {
  if (batchPreview.value.length === 0) {
    batchError.value = '沒有可新增的資料'
    return
  }
  
  batchSubmitting.value = true
  batchError.value = ''
  
  try {
    // Use batch API endpoint for better performance
    const response = await instance.post('/api/v1/datasets/batch', batchPreview.value)
    
    toast.success(`成功新增 ${response.data.length} 筆資料`)
    closeBatchModal()
    await fetchDatasets() // Refresh the list
    
  } catch (err) {
    const errorMsg = `批量新增失敗: ${err.response?.data?.detail || '未知錯誤'}`
    batchError.value = errorMsg
    toast.error(errorMsg)
    console.error('批量新增失敗:', err)
  } finally {
    batchSubmitting.value = false
  }
}

onMounted(fetchDatasets)

// 組件卸載時清理輪詢
onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-4 {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 