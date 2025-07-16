<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-800 mb-6">
      {{ isAdmin ? '系統統計儀表板' : '個人統計儀表板' }}
    </h1>

    <div v-if="loading" class="text-center">載入中...</div>
    <div v-else-if="error" class="text-red-500 bg-red-100 p-4 rounded-lg">{{ error }}</div>
    
    <div v-else-if="stats">
      <!-- KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-sm font-medium text-gray-500">
            {{ isAdmin ? '資料總筆數' : '已審核資料筆數' }}
          </h3>
          <p class="mt-2 text-3xl font-semibold text-gray-900">{{ stats.global_stats.total_datasets }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-sm font-medium text-gray-500">
            {{ isAdmin ? '總審核次數' : '我的審核次數' }}
          </h3>
          <p class="mt-2 text-3xl font-semibold text-gray-900">{{ stats.global_stats.total_reviews }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-sm font-medium text-gray-500">
            {{ isAdmin ? '通過率' : '我的通過率' }}
          </h3>
          <p class="mt-2 text-3xl font-semibold text-green-600">{{ acceptanceRate }}%</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-sm font-medium text-gray-500">
            {{ isAdmin ? '拒絕率' : '我的拒絕率' }}
          </h3>
          <p class="mt-2 text-3xl font-semibold text-red-600">{{ rejectionRate }}%</p>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <!-- Review Activity Chart -->
        <div class="lg:col-span-3 bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-lg font-medium text-gray-800 mb-4">
            {{ isAdmin ? '過去 30 天審核活動' : '過去 30 天我的審核活動' }}
          </h3>
          <div class="relative h-96">
            <Bar v-if="reviewActivityData.labels.length" :data="reviewActivityData" :options="chartOptions" />
          </div>
        </div>

        <!-- Top Lists -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Top Reviewers (only for admin) -->
          <div v-if="isAdmin" class="bg-white p-6 rounded-lg shadow-md">
            <h3 class="text-lg font-medium text-gray-800 mb-4">頂尖審核員</h3>
            <ul class="space-y-3">
              <li v-for="reviewer in stats.top_reviewers" :key="reviewer.username" class="flex justify-between items-center text-sm">
                <span class="font-medium text-gray-700">{{ reviewer.username }}</span>
                <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full font-semibold">{{ reviewer.review_count }} 次</span>
              </li>
              <li v-if="!stats.top_reviewers.length" class="text-gray-500 text-sm">尚無資料</li>
            </ul>
          </div>

          <!-- Common Rejection Reasons -->
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h3 class="text-lg font-medium text-gray-800 mb-4">
              {{ isAdmin ? '常見拒絕理由' : '我的拒絕理由' }}
            </h3>
            <ul class="space-y-3">
              <li v-for="reason in stats.common_rejection_reasons" :key="reason.reason" class="flex justify-between items-center text-sm">
                <span class="text-gray-700 truncate pr-4" :title="reason.reason">{{ reason.reason }}</span>
                <span class="px-2 py-1 bg-red-100 text-red-800 rounded-full font-semibold">{{ reason.count }} 次</span>
              </li>
              <li v-if="!stats.common_rejection_reasons.length" class="text-gray-500 text-sm">尚無資料</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import useAuth from '../store/auth';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const { instance, state } = useAuth();
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
    stats.value = response.data;
  } catch (err) {
    error.value = '無法獲取統計數據。';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const acceptanceRate = computed(() => {
  if (!stats.value || stats.value.global_stats.total_reviews === 0) return 0;
  return ((stats.value.global_stats.total_accepts / stats.value.global_stats.total_reviews) * 100).toFixed(1);
});

const rejectionRate = computed(() => {
  if (!stats.value || stats.value.global_stats.total_reviews === 0) return 0;
  return ((stats.value.global_stats.total_rejects / stats.value.global_stats.total_reviews) * 100).toFixed(1);
});

const reviewActivityData = computed(() => {
  if (!stats.value) return { labels: [], datasets: [] };
  return {
    labels: stats.value.review_activity.map(item => item.date.substring(5)), // Format date to "MM-DD"
    datasets: [{
      label: isAdmin.value ? '每日審核數量' : '我的每日審核數量',
      backgroundColor: '#4f46e5',
      borderColor: '#4f46e5',
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
        stepSize: 1
      }
    }
  },
  plugins: {
    legend: {
      display: false
    }
  }
};

onMounted(fetchStats);
</script> 