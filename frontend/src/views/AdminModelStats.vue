<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">模型統計管理</h1>
      <div class="flex space-x-4">
        <button 
          @click="showRefreshModal = true" 
          class="px-4 py-2 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors flex items-center space-x-2"
          :disabled="loading || refreshing"
          title="清空所有審核記錄並重新統計模型數據"
        >
          <svg v-if="refreshing" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span>{{ refreshing ? '重新統計中...' : '重新統計' }}</span>
        </button>
        <button 
          @click="exportCSV" 
          class="px-4 py-2 bg-teal-600 text-white font-semibold rounded-lg hover:bg-teal-700 transition-colors"
          :disabled="loading || modelStats.length === 0"
        >
          {{ loading ? '載入中...' : '匯出為 CSV' }}
        </button>
      </div>
    </div>

    <!-- 重新統計確認 Modal -->
    <div v-if="showRefreshModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div class="flex items-center mb-4">
          <svg class="h-6 w-6 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
          <h3 class="text-lg font-medium text-gray-900">確認重新統計</h3>
        </div>
        <div class="mb-6">
          <p class="text-gray-600 mb-2">您確定要執行重新統計嗎？</p>
          <div class="bg-red-50 border border-red-200 rounded-lg p-3">
            <p class="text-red-800 text-sm font-medium">⚠️ 警告：此操作將會：</p>
            <ul class="text-red-700 text-sm mt-2 space-y-1">
              <li>• 清空所有審核記錄</li>
              <li>• 重置所有資料集的審核狀態</li>
              <li>• 此操作不可逆轉</li>
            </ul>
          </div>
        </div>
        <div class="flex justify-end space-x-3">
          <button 
            @click="showRefreshModal = false"
            class="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            :disabled="refreshing"
          >
            取消
          </button>
          <button 
            @click="confirmRefreshStats"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center space-x-2"
            :disabled="refreshing"
          >
            <svg v-if="refreshing" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ refreshing ? '執行中...' : '確認執行' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-10">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-2 text-gray-500">載入模型統計中...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">載入失敗</h3>
          <p class="mt-1 text-sm text-red-700">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="modelStats.length === 0" class="text-center py-10 bg-white rounded-lg shadow-md">
      <div class="text-gray-400 text-6xl mb-4">📊</div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">沒有模型統計資料</h3>
      <p class="text-gray-500">目前沒有可用的模型統計資料。</p>
    </div>

    <!-- Model Statistics -->
    <div v-else class="space-y-6">
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-sm font-medium text-gray-500">總模型數</h3>
          <p class="mt-2 text-3xl font-semibold text-gray-900">{{ modelStats.length }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-sm font-medium text-gray-500">總資料集數</h3>
          <p class="mt-2 text-3xl font-semibold text-blue-600">{{ totalDatasets }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-sm font-medium text-gray-500">總審核次數</h3>
          <p class="mt-2 text-3xl font-semibold text-indigo-600">{{ totalReviews }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-sm font-medium text-gray-500">平均通過率</h3>
          <p class="mt-2 text-3xl font-semibold text-green-600">{{ averageAcceptanceRate }}%</p>
        </div>
      </div>

      <!-- Model Details Table -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">模型詳細統計</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  模型名稱
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  資料集數
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  審核次數
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  通過次數
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  拒絕次數
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  通過率
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  狀態
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="model in modelStats" :key="model.model_name" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-8 w-8">
                      <div class="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                        <span class="text-sm font-medium text-blue-600">{{ model.model_name.charAt(0).toUpperCase() }}</span>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ model.model_name }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ model.total_datasets }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ model.total_reviews }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                    {{ model.total_accepts }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">
                    {{ model.total_rejects }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                      <div 
                        class="bg-green-500 h-2 rounded-full" 
                        :style="{ width: `${model.acceptance_rate}%` }"
                      ></div>
                    </div>
                    <span class="text-sm font-medium text-gray-900">{{ model.acceptance_rate }}%</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      model.acceptance_rate >= 80 ? 'bg-green-100 text-green-800' :
                      model.acceptance_rate >= 60 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ 
                      model.acceptance_rate >= 80 ? '優秀' :
                      model.acceptance_rate >= 60 ? '良好' : '需改進'
                    }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Acceptance Rate Chart -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-lg font-medium text-gray-800 mb-4">模型通過率比較</h3>
          <div class="relative h-64">
            <Bar v-if="acceptanceRateData.labels.length" :data="acceptanceRateData" :options="chartOptions" />
          </div>
        </div>

        <!-- Dataset Count Chart -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-lg font-medium text-gray-800 mb-4">模型資料集數量</h3>
          <div class="relative h-64">
            <Doughnut v-if="datasetCountData.labels.length" :data="datasetCountData" :options="doughnutOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

const { instance } = useAuth()
const toast = useToast()
const modelStats = ref([])
const loading = ref(true)
const refreshing = ref(false)
const error = ref(null)
const showRefreshModal = ref(false)

const fetchModelStats = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await instance.get('/api/v1/stats/models')
    modelStats.value = response.data
  } catch (err) {
    console.error('Failed to load model stats:', err)
    error.value = '無法載入模型統計資料。'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const confirmRefreshStats = async () => {
  refreshing.value = true
  try {
    const response = await instance.post('/api/v1/stats/models/refresh')
    const result = response.data
    
    // 顯示主要成功訊息
    toast.success(result.message)
    
    // 如果有清理資訊，顯示詳細資訊
    if (result.cleanup_info) {
      const cleanupInfo = result.cleanup_info
      if (cleanupInfo.total_review_logs_cleared > 0) {
        toast.info(`已清空 ${cleanupInfo.total_review_logs_cleared} 筆審核記錄`)
      }
      if (cleanupInfo.raw_datasets_reset > 0) {
        toast.info(`已重置 ${cleanupInfo.raw_datasets_reset} 筆待審核資料的狀態`)
      }
    }
    
    // 顯示統計結果
    if (result.models && result.models.length > 0) {
      toast.info(`發現 ${result.model_count} 個模型：${result.models.join(', ')}`)
    }
    
    await fetchModelStats() // 重新載入資料
    showRefreshModal.value = false // 關閉確認 Modal
  } catch (err) {
    console.error('Failed to refresh stats:', err)
    toast.error('重新統計失敗：' + (err.response?.data?.detail || '未知錯誤'))
  } finally {
    refreshing.value = false
  }
}

const exportCSV = () => {
  if (modelStats.value.length === 0) {
    toast.info('沒有資料可匯出。')
    return
  }

  const headers = ['model_name', 'total_datasets', 'total_reviews', 'total_accepts', 'total_rejects', 'acceptance_rate']
  const csvRows = []
  
  // Add header row
  csvRows.push(headers.join(','))

  // Add data rows
  for (const row of modelStats.value) {
    const values = headers.map(header => {
      let cell = row[header]
      if (Array.isArray(cell) || (typeof cell === 'object' && cell !== null)) {
        cell = JSON.stringify(cell)
      }
      const escaped = ('' + (cell === null || cell === undefined ? '' : cell)).replace(/"/g, '""')
      return `"${escaped}"`
    })
    csvRows.push(values.join(','))
  }

  const csvString = csvRows.join('\n')
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', 'model_statistics.csv')
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

// Computed properties
const totalDatasets = computed(() => {
  return modelStats.value.reduce((sum, model) => sum + model.total_datasets, 0)
})

const totalReviews = computed(() => {
  return modelStats.value.reduce((sum, model) => sum + model.total_reviews, 0)
})

const averageAcceptanceRate = computed(() => {
  if (modelStats.value.length === 0) return 0
  const totalRate = modelStats.value.reduce((sum, model) => sum + model.acceptance_rate, 0)
  return (totalRate / modelStats.value.length).toFixed(1)
})

const acceptanceRateData = computed(() => {
  if (!modelStats.value.length) return { labels: [], datasets: [] }
  return {
    labels: modelStats.value.map(model => model.model_name),
    datasets: [{
      label: '通過率 (%)',
      backgroundColor: modelStats.value.map(model => 
        model.acceptance_rate >= 80 ? '#10B981' :
        model.acceptance_rate >= 60 ? '#F59E0B' : '#EF4444'
      ),
      borderColor: modelStats.value.map(model => 
        model.acceptance_rate >= 80 ? '#059669' :
        model.acceptance_rate >= 60 ? '#D97706' : '#DC2626'
      ),
      borderWidth: 1,
      data: modelStats.value.map(model => model.acceptance_rate)
    }]
  }
})

const datasetCountData = computed(() => {
  if (!modelStats.value.length) return { labels: [], datasets: [] }
  return {
    labels: modelStats.value.map(model => model.model_name),
    datasets: [{
      data: modelStats.value.map(model => model.total_datasets),
      backgroundColor: [
        '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
        '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
      ],
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      ticks: {
        callback: function(value) {
          return value + '%'
        }
      }
    }
  },
  plugins: {
    legend: {
      display: false
    }
  }
}

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom'
    }
  }
}

onMounted(fetchModelStats)
</script> 