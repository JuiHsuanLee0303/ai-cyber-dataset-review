<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">待審核資料集管理</h1>
      <button @click="openModal()" class="px-4 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700">
        新增資料
      </button>
    </div>

    <!-- Datasets Table -->
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full leading-normal">
        <thead>
          <tr>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">ID</th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">指令</th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">輸出</th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">通過</th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">不通過</th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="6" class="text-center py-10">載入中...</td></tr>
          <tr v-else-if="datasets.length === 0"><td colspan="6" class="text-center py-10">沒有資料。</td></tr>
          <tr v-else v-for="item in datasets" :key="item.id">
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">{{ item.id }}</td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm"><p class="truncate max-w-md">{{ item.instruction }}</p></td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm"><p class="truncate max-w-md">{{ item.output }}</p></td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-center text-green-600 font-semibold">{{ item.accept_count }}</td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-center">
              <button 
                @click="showRejections(item)" 
                :class="[item.reject_count > 0 ? 'text-red-600 hover:text-red-900 font-semibold' : 'text-gray-500 cursor-not-allowed']"
                :disabled="item.reject_count === 0"
              >
                {{ item.reject_count }}
              </button>
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
              <button @click="openModal(item)" class="text-indigo-600 hover:text-indigo-900 font-semibold mr-4">查看 / 編輯</button>
              <button @click="handleDelete(item.id)" class="text-red-600 hover:text-red-900">刪除</button>
            </td>
          </tr>
        </tbody>
      </table>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useAuth from '../store/auth'

const { instance } = useAuth()

const datasets = ref([])
const loading = ref(true)
const error = ref(null)

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

const fetchDatasets = async () => {
  loading.value = true
  try {
    const response = await instance.get('/api/v1/datasets/')
    datasets.value = response.data
  } catch (err) {
    error.value = '無法獲取資料列表。'
  } finally {
    loading.value = false
  }
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
  if (!confirm('確定要刪除這筆資料嗎？此操作無法復原。')) return
  error.value = null
  try {
    await instance.delete(`/api/v1/datasets/${id}`)
    await fetchDatasets()
  } catch (err) {
    error.value = `刪除失敗: ${err.response?.data?.detail || '未知錯誤'}`
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
    error.value = `無法獲取拒絕原因: ${err.response?.data?.detail || '未知錯誤'}`
  } finally {
    rejectionLoading.value = false
  }
}

const closeRejectionModal = () => {
  showRejectionModal.value = false
  rejectionReasons.value = []
  selectedDataset.value = null
}

onMounted(fetchDatasets)
</script> 