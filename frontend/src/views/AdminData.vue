<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">最終資料集管理</h1>
      <button @click="exportCSV" class="px-4 py-2 bg-teal-600 text-white font-semibold rounded-lg hover:bg-teal-700" :disabled="loading || finalDataset.length === 0">
        {{ loading ? '載入中...' : '匯出為 CSV' }}
      </button>
    </div>

    <!-- Final Dataset Table -->
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full leading-normal">
        <thead>
          <tr>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              ID
            </th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              指令 (Instruction)
            </th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              輸入 (Input)
            </th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              系統提示 (System)
            </th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              最終輸出 (Output)
            </th>
             <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              來源 (Source)
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="6" class="text-center py-10">載入中...</td></tr>
          <tr v-else-if="finalDataset.length === 0">
            <td colspan="6" class="text-center py-10 text-gray-500">
              目前沒有已通過審核的最終資料。
            </td>
          </tr>
          <tr v-else v-for="item in finalDataset" :key="item.id">
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              <p class="text-gray-900 whitespace-no-wrap">{{ item.id }}</p>
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              <p class="text-gray-900 whitespace-no-wrap truncate max-w-xs">{{ item.instruction }}</p>
            </td>
             <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              <p class="text-gray-900 whitespace-no-wrap truncate max-w-xs">{{ item.input }}</p>
            </td>
             <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              <p class="text-gray-900 whitespace-no-wrap truncate max-w-xs">{{ item.system }}</p>
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              <p class="text-gray-900 whitespace-no-wrap truncate max-w-md">{{ item.output }}</p>
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              <p class="text-gray-900 whitespace-no-wrap truncate max-w-xs">{{ item.source }}</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useAuth from '../store/auth'

const { instance } = useAuth()
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
    alert(error.value)
  } finally {
    loading.value = false
  }
}

const exportCSV = () => {
  if (finalDataset.value.length === 0) {
    alert('沒有資料可匯出。');
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