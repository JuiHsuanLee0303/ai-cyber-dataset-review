<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">最終資料集管理</h1>
      <button @click="exportCSV" class="px-4 py-2 bg-teal-600 text-white font-semibold rounded-lg hover:bg-teal-700" :disabled="loading || finalDataset.length === 0">
        {{ loading ? '載入中...' : '匯出為 CSV' }}
      </button>
    </div>

    <!-- Final Dataset Cards -->
    <div v-if="loading" class="text-center py-10">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto"></div>
      <p class="mt-2 text-gray-500">載入中...</p>
    </div>
    
    <div v-else-if="finalDataset.length === 0" class="text-center py-10 bg-white rounded-lg shadow-md">
      <div class="text-gray-400 text-6xl mb-4">✅</div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">沒有最終資料</h3>
      <p class="text-gray-500">目前沒有已通過審核的最終資料集。</p>
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
            <div class="text-xs text-gray-400">
              {{ new Date().toLocaleDateString() }}
            </div>
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
              最終輸出 (Output)
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
          
          <!-- Source (if exists) -->
          <div v-if="item.source && item.source.length > 0">
            <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <span class="w-2 h-2 bg-red-500 rounded-full mr-2"></span>
              來源 (Source)
            </h4>
            <div class="bg-gray-50 rounded-md p-3">
              <div class="space-y-1">
                <div v-for="(src, index) in item.source" :key="index" class="text-xs text-gray-600 bg-white px-2 py-1 rounded border">
                  {{ src }}
                </div>
              </div>
            </div>
          </div>
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

  const headers = ['id', 'instruction', 'input', 'output', 'system', 'source', 'history'];
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