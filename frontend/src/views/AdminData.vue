<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">最終資料集管理</h1>
      <div class="flex space-x-3">
        <button @click="exportCSV" class="px-4 py-2 bg-teal-600 text-white font-semibold rounded-lg hover:bg-teal-700 transition-colors" :disabled="loading || finalDataset.length === 0">
          {{ loading ? '載入中...' : '匯出為 CSV' }}
        </button>
        <button @click="showClearConfirm = true" class="px-4 py-2 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors" :disabled="loading || finalDataset.length === 0">
          清空所有資料
        </button>
      </div>
    </div>

    <!-- Final Dataset Cards -->
    <div v-if="loading" class="text-center py-10">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto"></div>
      <p class="mt-2 text-gray-500">載入中...</p>
    </div>
    
    <div v-else-if="finalDataset.length === 0" class="text-center py-10 bg-white rounded-lg shadow-md">
      <h3 class="text-3xl font-medium text-gray-900 mb-2">沒有最終資料</h3>
      <p class="text-gray-500 text-sm">目前沒有已通過審核的最終資料集。</p>
    </div>
    
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
      <div v-for="item in finalDataset" :key="item.id" class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
        <!-- Header -->
        <div class="p-4 border-b border-gray-200">
          <div class="flex justify-between items-center mb-3">
            <div class="flex items-center space-x-3">
              <span class="text-sm font-medium text-gray-500">#{{ item.id }}</span>
              <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                已通過
              </span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="text-xs text-gray-400">
                {{ new Date().toLocaleDateString() }}
              </div>
              <button 
                @click="deleteItem(item.id)" 
                class="p-1 text-red-500 hover:text-red-700 hover:bg-red-50 rounded transition-colors"
                title="刪除此筆資料"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Content -->
        <div class="p-4 space-y-4">
          <!-- Original Input -->
          <div>
            <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              原始輸入 (Original Input)
            </h4>
            <div class="bg-gray-50 rounded-md p-3">
              <p class="text-sm text-gray-800 line-clamp-3">{{ item.original_input || '無' }}</p>
            </div>
          </div>
          
          <!-- Final Output -->
          <div>
            <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
              最終輸出 (Final Output)
            </h4>
            <div class="bg-gray-50 rounded-md p-3">
              <p class="text-sm text-gray-800 line-clamp-4">{{ item.final_output || '無' }}</p>
            </div>
          </div>
          

          
          <!-- Model Name (if exists) -->
          <div v-if="item.model_name">
            <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <span class="w-2 h-2 bg-indigo-500 rounded-full mr-2"></span>
              生成模型 (Model)
            </h4>
            <div class="bg-gray-50 rounded-md p-3">
              <span class="text-sm text-gray-800 font-medium">{{ item.model_name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Clear All Confirmation Modal -->
    <div v-if="showClearConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md mx-4">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900">確認清空</h3>
        </div>
        <p class="text-gray-600 mb-6">
          您確定要清空所有最終資料集嗎？此操作無法撤銷，所有資料將永久刪除。
        </p>
        <div class="flex justify-end space-x-3">
          <button 
            @click="showClearConfirm = false" 
            class="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            取消
          </button>
          <button 
            @click="clearAllData" 
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            :disabled="clearing"
          >
            {{ clearing ? '清空中...' : '確認清空' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Item Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md mx-4">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900">確認刪除</h3>
        </div>
        <p class="text-gray-600 mb-6">
          您確定要刪除此筆最終資料集嗎？此操作無法撤銷。
        </p>
        <div class="flex justify-end space-x-3">
          <button 
            @click="showDeleteConfirm = false" 
            class="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            取消
          </button>
          <button 
            @click="confirmDeleteItem" 
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            :disabled="deleting"
          >
            {{ deleting ? '刪除中...' : '確認刪除' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'

const { instance } = useAuth()
const toast = useToast()
const finalDataset = ref([])
const loading = ref(true)
const error = ref(null)
const showClearConfirm = ref(false)
const showDeleteConfirm = ref(false)
const clearing = ref(false)
const deleting = ref(false)
const itemToDelete = ref(null)

const fetchFinalDataset = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await instance.get('/api/v1/datasets/final')
    finalDataset.value = response.data
  } catch (err) {
    console.error('Failed to load final dataset:', err)
    error.value = '無法載入最終資料集。'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const exportCSV = () => {
  if (finalDataset.value.length === 0) {
    toast.info('沒有資料可匯出。');
    return;
  }

  const headers = ['id', 'original_input', 'final_output', 'raw_dataset_id', 'model_name'];
  const csvRows = [];
  
  // Add header row
  csvRows.push(headers.join(','));

  // Add data rows
  for (const row of finalDataset.value) {
    const values = headers.map(header => {
      let cell = row[header];
      if (Array.isArray(cell) || (typeof cell === 'object' && cell !== null)) {
        cell = JSON.stringify(cell);
      }
      const escaped = ('' + (cell === null || cell === undefined ? '' : cell)).replace(/"/g, '""');
      return `"${escaped}"`;
    });
    csvRows.push(values.join(','));
  }

  const csvString = csvRows.join('\n');
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'final_dataset.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

const deleteItem = (itemId) => {
  itemToDelete.value = itemId
  showDeleteConfirm.value = true
}

const confirmDeleteItem = async () => {
  if (!itemToDelete.value) return
  
  deleting.value = true
  try {
    await instance.delete(`/api/v1/datasets/final/${itemToDelete.value}`)
    toast.success('資料刪除成功')
    await fetchFinalDataset() // 重新載入資料
  } catch (err) {
    console.error('Failed to delete item:', err)
    toast.error('刪除失敗：' + (err.response?.data?.detail || '未知錯誤'))
  } finally {
    deleting.value = false
    showDeleteConfirm.value = false
    itemToDelete.value = null
  }
}

const clearAllData = async () => {
  clearing.value = true
  try {
    const response = await instance.delete('/api/v1/datasets/final')
    toast.success(`成功清空 ${response.data.deleted_count} 筆資料`)
    await fetchFinalDataset() // 重新載入資料
  } catch (err) {
    console.error('Failed to clear all data:', err)
    toast.error('清空失敗：' + (err.response?.data?.detail || '未知錯誤'))
  } finally {
    clearing.value = false
    showClearConfirm.value = false
  }
}

onMounted(fetchFinalDataset)
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