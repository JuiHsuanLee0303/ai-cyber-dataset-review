<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold text-gray-800 mb-6">資料審核</h1>
    
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
    <div v-else class="bg-white p-8 rounded-lg shadow-md space-y-6">
      <!-- System Prompt -->
      <div v-if="currentItem.system">
        <h2 class="text-lg font-semibold text-gray-500 mb-2">系統提示 (System)</h2>
        <div class="p-3 bg-gray-100 rounded-md text-gray-800 whitespace-pre-wrap font-mono text-sm">
          {{ currentItem.system }}
        </div>
      </div>

      <!-- Instruction -->
      <div>
        <h2 class="text-lg font-semibold text-gray-700 mb-2">指令 (Instruction)</h2>
        <div class="p-3 bg-gray-100 rounded-md text-gray-800 whitespace-pre-wrap font-mono text-sm">
          {{ currentItem.instruction }}
        </div>
      </div>
      
      <!-- Input -->
      <div v-if="currentItem.input">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">輸入內容 (Input)</h2>
        <div class="p-3 bg-gray-100 rounded-md text-gray-800 whitespace-pre-wrap font-mono text-sm">
          {{ currentItem.input }}
        </div>
      </div>
      
      <!-- History -->
      <div v-if="currentItem.history && currentItem.history.length > 0">
        <h2 class="text-lg font-semibold text-gray-500 mb-2">歷史紀錄 (History)</h2>
        <div class="p-3 bg-gray-100 rounded-md space-y-2">
            <div v-for="(turn, index) in currentItem.history" :key="index" class="text-sm">
                <p class="font-semibold text-gray-600">{{ turn.role }}:</p>
                <p class="whitespace-pre-wrap font-mono text-gray-800">{{ turn.content }}</p>
            </div>
        </div>
      </div>

      <!-- Source -->
      <div v-if="currentItem.source && currentItem.source.length > 0">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">資料來源 (Source)</h2>
        <ul class="list-disc list-inside bg-gray-100 p-3 rounded-md text-sm">
          <li v-for="(src, index) in currentItem.source" :key="index" class="text-gray-600">{{ src }}</li>
        </ul>
      </div>

      <!-- Generated Output -->
      <div>
        <h2 class="text-xl font-bold text-blue-800 mb-2">AI 生成內容 (Output)</h2>
        <div class="p-4 bg-blue-50 border-2 border-blue-200 rounded-md text-gray-900 whitespace-pre-wrap font-mono">
          {{ currentItem.output }}
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="pt-6 border-t flex justify-between items-center">
        <div class="text-sm text-gray-500">
          進度: {{ currentIndex + 1 }} / {{ datasets.length }}
        </div>
        <div class="flex space-x-4">
          <button @click="showRejectModal = true" class="px-6 py-2 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition-colors duration-200">
            拒絕 (Reject)
          </button>
          <button @click="handleAccept" class="px-6 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition-colors duration-200">
            接受 (Accept)
          </button>
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
        <button @click="nextItem" class="px-8 py-3 bg-gray-400 text-white font-bold rounded-lg hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-opacity-50 transition-colors duration-200">
          跳過此筆
        </button>
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import useAuth from '../store/auth'

const { instance } = useAuth()

const loading = ref(true)
const showRejectModal = ref(false)
const rejectComment = ref('')
const datasets = ref([])
const currentIndex = ref(0)

const currentItem = computed(() => {
  if (datasets.value.length > 0 && currentIndex.value < datasets.value.length) {
    return datasets.value[currentIndex.value]
  }
  return null
})

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

  } catch (error) {
    console.error('Failed to load datasets:', error)
    alert('載入待審核資料失敗。')
  } finally {
    loading.value = false
  }
}

const nextItem = () => {
  if (currentIndex.value < datasets.value.length - 1) {
    currentIndex.value++
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
    nextItem() // Move to the next item
  } catch (error) {
     console.error('Failed to submit review:', error)
     alert(`提交審核失敗: ${error.response?.data?.detail || '未知錯誤'}`)
  }
}

const handleAccept = () => {
  submitReview('ACCEPT')
}

const handleReject = () => {
  if (!rejectComment.value) {
    alert('請填寫拒絕原因。')
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