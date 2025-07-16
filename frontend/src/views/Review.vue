<template>
  <div class="max-w-5xl mx-auto">
    <h1 class="text-3xl font-bold text-gray-800 mb-6">資料審核</h1>
    
    <!-- 資料集結構說明 -->
    <div class="mb-8 bg-blue-50 border-l-4 border-blue-400 p-6 rounded-r-lg">
      <h2 class="text-lg font-semibold text-blue-800 mb-3">📋 指令微調資料集結構說明</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-700">
        <div class="space-y-2">
          <p><strong>Instruction（指令）：</strong>告訴 AI 模型要執行什麼任務，例如「總結這段文字」或「生成 Python 函式」</p>
          <p><strong>Input（輸入）：</strong>提供給指令的上下文或原始內容，可能是文章段落、程式碼片段或其他資料</p>
        </div>
        <div class="space-y-2">
          <p><strong>Output（輸出）：</strong>期望 AI 模型回覆的正確答案或內容</p>
          <p><strong>Source（來源）：</strong>生成這筆資料的法規依據，確保內容符合資安法規要求</p>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="text-center p-12">
      <p class="text-gray-500">載入中...</p>
    </div>

    <div v-else-if="!currentItem" class="text-center p-12 bg-white rounded-lg shadow-md">
      <h2 class="text-2xl font-bold text-gray-700">太棒了！</h2>
      <p class="mt-2 text-gray-600">目前沒有更多待審核的資料了。</p>
      <button @click="fetchDatasets" class="mt-6 px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700">
        重新載入
      </button>
    </div>

    <!-- Data Card -->
    <div v-else class="bg-white p-8 rounded-lg shadow-md space-y-8">
      <!-- Status Display -->
      <div class="flex justify-between items-center pb-4 border-b border-gray-200">
        <div class="flex items-center space-x-4">
          <!-- 重新生成中狀態 -->
          <div v-if="currentItem.review_status === 'regenerating'" class="flex items-center space-x-2">
            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-orange-500"></div>
            <span class="px-3 py-1 bg-orange-100 text-orange-800 text-sm font-medium rounded-full">
              🔄 重新生成中
            </span>
          </div>
          <!-- 一般待審核狀態 -->
          <span v-else class="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
            📋 待審核
          </span>
          <span class="text-sm text-gray-500">
            資料 ID: {{ currentItem.id }}
          </span>
        </div>
        <div class="text-sm text-gray-500">
          審核統計: 通過 {{ currentItem.accept_count }} | 拒絕 {{ currentItem.reject_count }}
        </div>
      </div>
      <!-- System Prompt -->
      <div v-if="currentItem.system" class="border-l-4 border-purple-400 pl-4">
        <div class="flex items-center mb-3">
          <h2 class="text-lg font-semibold text-purple-700">系統提示 (System Prompt)</h2>
          <span class="ml-2 px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">可選</span>
        </div>
        <p class="text-sm text-gray-600 mb-3">設定 AI 模型的角色和行為準則，例如「你是一位資安專家，專門協助處理資通安全相關問題」</p>
        <div class="p-4 bg-purple-50 border border-purple-200 rounded-md text-gray-800 whitespace-pre-wrap font-mono text-sm">
          {{ currentItem.system }}
        </div>
      </div>

      <!-- Instruction -->
      <div class="border-l-4 border-green-400 pl-4">
        <div class="flex items-center mb-3">
          <h2 class="text-lg font-semibold text-green-700">指令 (Instruction)</h2>
          <span class="ml-2 px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">必填</span>
        </div>
        <p class="text-sm text-gray-600 mb-3">明確告訴 AI 模型要執行什麼任務，例如「根據資安法規分析這段程式碼的安全性」或「生成符合資通安全管理法要求的資安政策」</p>
        <div class="p-4 bg-green-50 border border-green-200 rounded-md text-gray-800 whitespace-pre-wrap font-mono text-sm">
          {{ currentItem.instruction }}
        </div>
      </div>
      
      <!-- Input -->
      <div v-if="currentItem.input" class="border-l-4 border-blue-400 pl-4">
        <div class="flex items-center mb-3">
          <h2 class="text-lg font-semibold text-blue-700">輸入內容 (Input)</h2>
          <span class="ml-2 px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">可選</span>
        </div>
        <p class="text-sm text-gray-600 mb-3">提供給指令的上下文或原始資料，可能是程式碼、文件內容、資安事件描述等，讓 AI 模型有足夠資訊來執行指令</p>
        <div class="p-4 bg-blue-50 border border-blue-200 rounded-md text-gray-800 whitespace-pre-wrap font-mono text-sm">
          {{ currentItem.input }}
        </div>
      </div>
      
      <!-- History -->
      <div v-if="currentItem.history && currentItem.history.length > 0" class="border-l-4 border-orange-400 pl-4">
        <div class="flex items-center mb-3">
          <h2 class="text-lg font-semibold text-orange-700">對話歷史 (History)</h2>
          <span class="ml-2 px-2 py-1 bg-orange-100 text-orange-700 text-xs rounded-full">可選</span>
        </div>
        <p class="text-sm text-gray-600 mb-3">多輪對話的歷史記錄，包含用戶和 AI 的先前對話內容，用於維持對話的連續性和上下文</p>
        <div class="p-4 bg-orange-50 border border-orange-200 rounded-md space-y-3">
            <div v-for="(turn, index) in currentItem.history" :key="index" class="text-sm">
                <p class="font-semibold text-orange-600 mb-1">{{ turn.role === 'user' ? '👤 用戶' : '🤖 AI' }}:</p>
                <p class="whitespace-pre-wrap font-mono text-gray-800 bg-white p-2 rounded border">{{ turn.content }}</p>
            </div>
        </div>
      </div>

      <!-- Source -->
      <div v-if="currentItem.source && currentItem.source.length > 0" class="border-l-4 border-red-400 pl-4">
        <div class="flex items-center mb-3">
          <h2 class="text-lg font-semibold text-red-700">法規來源 (Source)</h2>
          <span class="ml-2 px-2 py-1 bg-red-100 text-red-700 text-xs rounded-full">必填</span>
        </div>
        <p class="text-sm text-gray-600 mb-3">生成這筆資料所依據的資安法規條文，確保 AI 模型的回答符合法規要求，具有法律依據</p>
        <div class="bg-red-50 border border-red-200 p-4 rounded-md space-y-4">
          <div v-for="(src, index) in currentItem.source" :key="index" class="text-sm">
            <div class="flex items-start space-x-3">
              <span class="text-red-500 mt-1 text-lg">📜</span>
              <div class="flex-1">
                <div class="text-red-700 font-medium bg-white p-2 rounded border">{{ src }}</div>
                <div v-if="sourceDetails[index]" class="mt-3 p-3 bg-white rounded border-l-4 border-red-500">
                  <div class="text-xs text-gray-500 mb-2 font-semibold">📋 法規條文內容：</div>
                  <div class="text-gray-800 whitespace-pre-wrap text-sm">{{ sourceDetails[index].content }}</div>
                </div>
                <div v-else-if="sourceLoading[index]" class="mt-3 text-xs text-gray-500 flex items-center">
                  <span class="animate-spin mr-2">⏳</span> 載入法規內容中...
                </div>
                <div v-else-if="sourceErrors[index]" class="mt-3 text-xs text-red-500 flex items-center">
                  <span class="mr-2">❌</span> 無法載入法規內容
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Generated Output -->
      <div class="border-l-4 border-indigo-400 pl-4">
        <div class="flex items-center mb-3">
          <h2 class="text-xl font-bold text-indigo-700">AI 生成內容 (Output)</h2>
          <span class="ml-2 px-2 py-1 bg-indigo-100 text-indigo-700 text-xs rounded-full">必填</span>
        </div>
        <p class="text-sm text-gray-600 mb-3">根據指令和輸入內容，AI 模型應該產生的正確回答或內容，這將作為訓練資料的標準答案</p>
        <div class="p-4 bg-indigo-50 border-2 border-indigo-200 rounded-md text-gray-900 whitespace-pre-wrap font-mono text-sm">
          {{ currentItem.output }}
        </div>
      </div>

      <!-- 審核重點提示 -->
      <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r-lg">
        <h3 class="text-lg font-semibold text-yellow-800 mb-2">🔍 審核重點</h3>
        <div class="text-sm text-yellow-700 space-y-1">
          <p>• <strong>指令明確性：</strong>指令是否清楚明確，AI 模型能理解要執行什麼任務？</p>
          <p>• <strong>內容準確性：</strong>AI 生成的內容是否符合資安法規要求？</p>
          <p>• <strong>法規依據：</strong>資料來源是否正確，法規條文是否相關？</p>
          <p>• <strong>實用性：</strong>這筆資料是否對資安實務有幫助？</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="pt-6 border-t flex justify-between items-center">
        <div class="text-sm text-gray-500">
          進度: {{ currentIndex + 1 }} / {{ datasets.length }}
        </div>
        <div class="flex space-x-4">
          <!-- 重新生成中時顯示提示 -->
          <div v-if="currentItem.review_status === 'regenerating'" class="flex items-center space-x-2">
            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-orange-500"></div>
            <span class="text-orange-600 font-medium">正在重新生成中，請稍候...</span>
          </div>
          <!-- 正常審核按鈕 -->
          <div v-else class="flex space-x-4">
            <button @click="showRejectModal = true" class="px-6 py-2 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition-colors duration-200">
              拒絕 (Reject)
            </button>
            <button @click="handleAccept" class="px-6 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition-colors duration-200">
              接受 (Accept)
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Reject Modal -->
    <div v-if="showRejectModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">拒絕原因</h3>
        <textarea 
          v-model="rejectComment"
          rows="4"
          class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="請說明拒絕這筆生成資料的原因..."
        ></textarea>
        <div class="mt-6 flex justify-end space-x-4">
          <button @click="showRejectModal = false" class="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400">
            取消
          </button>
          <button @click="handleReject" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
            確認拒絕
          </button>
        </div>
      </div>
    </div>

    <!-- Next button -->
     <div v-if="currentItem && !loading" class="mt-6 text-center">
        <button 
          @click="nextItem" 
          :disabled="currentItem.review_status === 'regenerating'"
          :class="[
            'px-8 py-3 font-bold rounded-lg focus:outline-none focus:ring-2 focus:ring-opacity-50 transition-colors duration-200',
            currentItem.review_status === 'regenerating' 
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
              : 'bg-gray-400 text-white hover:bg-gray-500 focus:ring-gray-300'
          ]"
        >
          {{ currentItem.review_status === 'regenerating' ? '重新生成中...' : '跳過此筆' }}
        </button>
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'

const { instance } = useAuth()
const toast = useToast()

const loading = ref(true)
const showRejectModal = ref(false)
const rejectComment = ref('')
const datasets = ref([])
const currentIndex = ref(0)
const sourceDetails = ref({})
const sourceLoading = ref({})
const sourceErrors = ref({})

const currentItem = computed(() => {
  if (datasets.value.length > 0 && currentIndex.value < datasets.value.length) {
    return datasets.value[currentIndex.value]
  }
  return null
})

// 解析資料來源字串，提取法規標題和條號
const parseSource = (sourceStr) => {
  // 範例: "公務機關所屬人員資通安全事項獎懲辦法第1條"
  const match = sourceStr.match(/^(.+?)第(\d+)條$/)
  if (match) {
    return {
      title: match[1].trim(),
      number: match[2]
    }
  }
  return null
}

// 載入法規文章內容
const loadSourceDetails = async (sourceStr, index) => {
  const parsed = parseSource(sourceStr)
  if (!parsed) {
    sourceErrors.value[index] = '無法解析法規格式'
    return
  }

  sourceLoading.value[index] = true
  sourceErrors.value[index] = null
  
  try {
    const response = await instance.get('/api/v1/legal-articles/search', {
      params: {
        title: parsed.title,
        number: parsed.number
      }
    })
    sourceDetails.value[index] = response.data
  } catch (error) {
    console.error('Failed to load legal article:', error)
    sourceErrors.value[index] = '法規不存在或載入失敗'
  } finally {
    sourceLoading.value[index] = false
  }
}

// 當當前項目改變時，載入資料來源詳情
const loadCurrentItemSources = async () => {
  if (!currentItem.value || !currentItem.value.source) return
  
  // 清理之前的狀態
  sourceDetails.value = {}
  sourceLoading.value = {}
  sourceErrors.value = {}
  
  // 為每個資料來源載入詳情
  for (let i = 0; i < currentItem.value.source.length; i++) {
    await loadSourceDetails(currentItem.value.source[i], i)
  }
}

const fetchDatasets = async () => {
  loading.value = true
  datasets.value = []
  currentIndex.value = 0
  try {
    // For now, we fetch all datasets. In a real app, you'd likely fetch only those needing review.
    const response = await instance.get('/api/v1/datasets/') 
    // A simple filter to find items the current user hasn't reviewed.
    // This is a placeholder and has performance implications on the frontend.
    // Ideally, the backend should provide an endpoint for this.
    const res = await instance.get('/api/v1/auth/me');
    const currentUser = res.data;
    
    datasets.value = response.data.filter(d => {
        return !d.review_logs.some(log => log.reviewer_id === currentUser.id);
    });

    // 載入第一個項目的資料來源
    if (datasets.value.length > 0) {
      await loadCurrentItemSources()
    }

  } catch (error) {
    console.error('Failed to load datasets:', error)
    toast.error('載入待審核資料失敗。')
  } finally {
    loading.value = false
  }
}

const nextItem = async () => {
  if (currentIndex.value < datasets.value.length - 1) {
    currentIndex.value++
    // 載入新項目的資料來源
    await loadCurrentItemSources()
  } else {
    // Reached the end
    currentIndex.value = datasets.value.length
    // Optionally show a message or fetch more data
  }
}

const submitReview = async (result, comment = null) => {
  if (!currentItem.value) return
  
  try {
    await instance.post(`/api/v1/review/${currentItem.value.id}`, {
      result: result,
      comment: comment
    })
    toast.success('審核結果已提交！');
    nextItem() // Move to the next item
  } catch (error) {
     console.error('Failed to submit review:', error)
     toast.error(`提交審核失敗: ${error.response?.data?.detail || '未知錯誤'}`)
  }
}

const handleAccept = () => {
  submitReview('ACCEPT')
}

const handleReject = () => {
  if (!rejectComment.value) {
    toast.warning('請填寫拒絕原因。');
    return
  }
  submitReview('REJECT', rejectComment.value)
  showRejectModal.value = false
  rejectComment.value = ''
}

onMounted(() => {
  fetchDatasets()
})
</script> 