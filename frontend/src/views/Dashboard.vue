<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header Section -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">
        {{ isAdmin ? '系統統計儀表板' : '個人統計儀表板' }}
      </h1>
      <div class="flex space-x-4">
        <div class="flex items-center space-x-2 bg-white px-4 py-2 rounded-full shadow-sm">
          <div class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
          <span class="text-sm text-gray-600">即時更新</span>
        </div>
        <button 
          @click="fetchStats" 
          :disabled="loading"
          class="flex items-center space-x-2 bg-white px-4 py-2 rounded-full shadow-sm hover:shadow-md transition-all duration-200 disabled:opacity-50"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span class="text-sm">重新整理</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="text-center">
        <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p class="text-gray-600 text-lg">載入統計數據中...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 mb-6">
      <div class="flex items-center space-x-3">
        <div class="flex-shrink-0">
          <svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-medium text-red-800">載入失敗</h3>
          <p class="text-red-700 mt-1">{{ error }}</p>
        </div>
      </div>
    </div>
    
    <!-- Main Content -->
    <div v-else-if="stats && stats.global_stats" class="space-y-8">
      <!-- KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="group bg-white p-6 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100">
          <div class="flex items-center justify-between mb-4">
            <div class="p-3 bg-blue-100 rounded-xl">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-gray-900">{{ stats.global_stats.total_datasets || 0 }}</div>
              <div class="text-sm text-gray-500">{{ isAdmin ? '資料總筆數' : '已審核資料筆數' }}</div>
            </div>
          </div>
          <div class="flex items-center text-sm">
            <span class="text-green-600 font-medium">+12%</span>
            <span class="text-gray-500 ml-2">較上月</span>
          </div>
        </div>

        <div class="group bg-white p-6 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100">
          <div class="flex items-center justify-between mb-4">
            <div class="p-3 bg-green-100 rounded-xl">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-gray-900">{{ stats.global_stats.total_reviews || 0 }}</div>
              <div class="text-sm text-gray-500">{{ isAdmin ? '總審核次數' : '我的審核次數' }}</div>
            </div>
          </div>
          <div class="flex items-center text-sm">
            <span class="text-green-600 font-medium">+8%</span>
            <span class="text-gray-500 ml-2">較上月</span>
          </div>
        </div>

        <div class="group bg-white p-6 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-4">
            <div class="p-3 bg-emerald-100 rounded-xl">
              <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-emerald-600">{{ acceptanceRate }}%</div>
              <div class="text-sm text-gray-500">{{ isAdmin ? '通過率' : '我的通過率' }}</div>
            </div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-emerald-500 h-2 rounded-full transition-all duration-500" :style="{ width: acceptanceRate + '%' }"></div>
          </div>
        </div>

        <div class="group bg-white p-6 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-4">
            <div class="p-3 bg-red-100 rounded-xl">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"></path>
              </svg>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-red-600">{{ rejectionRate }}%</div>
              <div class="text-sm text-gray-500">{{ isAdmin ? '拒絕率' : '我的拒絕率' }}</div>
            </div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-red-500 h-2 rounded-full transition-all duration-500" :style="{ width: rejectionRate + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div v-if="stats.review_activity && stats.review_activity.length > 0" class="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <!-- Review Activity Chart -->
        <div class="lg:col-span-3 bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-xl font-semibold text-gray-900">
                {{ isAdmin ? '過去 30 天審核活動' : '過去 30 天我的審核活動' }}
              </h3>
              <p class="text-gray-500 text-sm mt-1">每日審核數量趨勢</p>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span class="text-sm text-gray-600">審核數量</span>
            </div>
          </div>
          <div class="relative h-80">
            <Bar v-if="reviewActivityData.labels.length" :data="reviewActivityData" :options="chartOptions" />
          </div>
        </div>

        <!-- Sidebar Cards -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Top Reviewers (only for admin) -->
          <div v-if="isAdmin && stats.top_reviewers" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div class="flex items-center space-x-3 mb-6">
              <div class="p-2 bg-purple-100 rounded-lg">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900">頂尖審核員</h3>
            </div>
            <div class="space-y-4">
              <div v-for="(reviewer, index) in stats.top_reviewers" :key="reviewer.username" 
                   class="flex items-center space-x-4 p-3 rounded-xl hover:bg-gray-50 transition-colors duration-200">
                <div class="flex items-center justify-center w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full font-semibold text-sm">
                  {{ index + 1 }}
                </div>
                <div class="flex-1">
                  <div class="font-medium text-gray-900">{{ reviewer.username }}</div>
                  <div class="text-sm text-gray-500">{{ reviewer.review_count }} 次審核</div>
                </div>
                <div class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                  {{ reviewer.review_count }}
                </div>
              </div>
              <div v-if="!stats.top_reviewers.length" class="text-center py-8 text-gray-500">
                <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <p>尚無資料</p>
              </div>
            </div>
          </div>
          
          <!-- Model Statistics (only for admin) -->
          <div v-if="isAdmin && stats.model_stats && stats.model_stats.length > 0" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div class="flex items-center space-x-3 mb-6">
              <div class="p-2 bg-indigo-100 rounded-lg">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900">模型統計</h3>
            </div>
            <div class="space-y-4">
              <div v-for="model in stats.model_stats" :key="model.model_name" 
                   class="p-4 rounded-xl border border-gray-100 hover:border-indigo-200 transition-colors duration-200">
                <div class="flex items-center justify-between mb-2">
                  <span class="font-medium text-gray-900">{{ model.model_name }}</span>
                  <span class="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-medium">
                    {{ model.acceptance_rate }}%
                  </span>
                </div>
                <div class="flex items-center justify-between text-sm text-gray-500">
                  <span>{{ model.total_datasets }} 筆資料</span>
                  <span>{{ model.total_reviews }} 次審核</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Common Rejection Reasons -->
          <div v-if="stats.common_rejection_reasons" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div class="flex items-center space-x-3 mb-6">
              <div class="p-2 bg-red-100 rounded-lg">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900">
                {{ isAdmin ? '常見拒絕理由' : '我的拒絕理由' }}
              </h3>
            </div>
            <div class="space-y-3">
              <div v-for="reason in stats.common_rejection_reasons" :key="reason.reason" 
                   class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 transition-colors duration-200">
                <span class="text-gray-700 truncate pr-4 flex-1" :title="reason.reason">{{ reason.reason }}</span>
                <span class="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-medium flex-shrink-0">
                  {{ reason.count }} 次
                </span>
              </div>
              <div v-if="!stats.common_rejection_reasons.length" class="text-center py-8 text-gray-500">
                <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <p>尚無拒絕記錄</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Data State -->
      <div v-else class="text-center py-16 bg-white rounded-2xl shadow-sm border border-gray-100">
        <div class="w-24 h-24 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">尚無統計數據</h3>
        <p class="text-gray-500 mb-6">目前沒有審核活動數據可供顯示。</p>
        <button @click="fetchStats" class="inline-flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span>重新載入</span>
        </button>
      </div>
    </div>

    <!-- Fallback State -->
    <div v-else class="text-center py-16 bg-white rounded-2xl shadow-sm border border-gray-100">
      <div class="w-24 h-24 bg-gradient-to-r from-red-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-12 h-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">數據載入失敗</h3>
      <p class="text-gray-500 mb-6">無法載入統計數據，請重新整理頁面。</p>
      <button @click="fetchStats" class="inline-flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-red-600 to-pink-600 text-white rounded-xl hover:from-red-700 hover:to-pink-700 transition-all duration-200 shadow-lg hover:shadow-xl">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        <span>重新載入</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import useAuth from '../store/auth';
import { useToast } from 'vue-toastification';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { palette } from '@/themes/palette';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const { instance, state } = useAuth();
const toast = useToast();
const stats = ref(null);
const loading = ref(true);
const error = ref(null);

// 計算屬性：判斷是否為管理員
const isAdmin = computed(() => {
  return state.user && state.user.role === 'admin';
});

const fetchStats = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await instance.get('/api/v1/stats/');
    if (response.data) {
      stats.value = response.data;
      toast.success('統計數據已更新！');
    } else {
      error.value = '獲取統計數據失敗：數據格式錯誤';
      toast.error('獲取統計數據失敗：數據格式錯誤');
    }
  } catch (err) {
    console.error('Stats API error:', err);
    if (err.response?.status === 401) {
      error.value = '認證失敗，請重新登入';
      toast.error('認證失敗，請重新登入');
    } else if (err.response?.status === 500) {
      error.value = '伺服器錯誤，請稍後再試';
      toast.error('伺服器錯誤，請稍後再試');
    } else {
      error.value = '無法獲取統計數據，請檢查網路連接';
      toast.error('無法獲取統計數據，請檢查網路連接');
    }
  } finally {
    loading.value = false;
  }
};

const acceptanceRate = computed(() => {
  if (!stats.value || !stats.value.global_stats || stats.value.global_stats.total_reviews === 0) return 0;
  return ((stats.value.global_stats.total_accepts / stats.value.global_stats.total_reviews) * 100).toFixed(1);
});

const rejectionRate = computed(() => {
  if (!stats.value || !stats.value.global_stats || stats.value.global_stats.total_reviews === 0) return 0;
  return ((stats.value.global_stats.total_rejects / stats.value.global_stats.total_reviews) * 100).toFixed(1);
});

const reviewActivityData = computed(() => {
  if (!stats.value || !stats.value.review_activity) return { labels: [], datasets: [] };
  return {
    labels: stats.value.review_activity.map(item => item.date.substring(5)), // Format date to "MM-DD"
    datasets: [{
      label: isAdmin.value ? '每日審核數量' : '我的每日審核數量',
      backgroundColor: 'rgba(59, 130, 246, 0.8)',
      borderColor: 'rgba(59, 130, 246, 1)',
      borderWidth: 2,
      borderRadius: 8,
      borderSkipped: false,
      data: stats.value.review_activity.map(item => item.count),
    }]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1,
        color: '#6B7280',
        font: {
          size: 12
        }
      },
      grid: {
        color: '#E5E7EB',
        drawBorder: false
      }
    },
    x: {
      ticks: {
        color: '#6B7280',
        font: {
          size: 12
        }
      },
      grid: {
        display: false
      }
    }
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#FFFFFF',
      bodyColor: '#FFFFFF',
      borderColor: 'rgba(59, 130, 246, 0.5)',
      borderWidth: 1,
      cornerRadius: 8,
      displayColors: false,
      callbacks: {
        title: function(context) {
          return `日期: ${context[0].label}`;
        },
        label: function(context) {
          return `審核數量: ${context.parsed.y} 次`;
        }
      }
    }
  },
  interaction: {
    intersect: false,
    mode: 'index'
  },
  elements: {
    bar: {
      hoverBackgroundColor: 'rgba(59, 130, 246, 1)'
    }
  }
};

onMounted(fetchStats);
</script>

<style scoped>
/* 添加自定義動畫效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.group {
  animation: fadeInUp 0.6s ease-out;
}

.group:nth-child(1) { animation-delay: 0.1s; }
.group:nth-child(2) { animation-delay: 0.2s; }
.group:nth-child(3) { animation-delay: 0.3s; }
.group:nth-child(4) { animation-delay: 0.4s; }

/* 滾動條樣式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style> 