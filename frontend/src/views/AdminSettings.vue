<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-800 mb-6">系統設定</h1>
    
    <div v-if="loading" class="text-center">載入中...</div>
    <div v-else-if="error" class="text-red-500 bg-red-100 p-4 rounded-lg">{{ error }}</div>
    
    <div v-else class="bg-white p-8 rounded-lg shadow-md max-w-2xl">
      <form @submit.prevent="saveSettings">
        
        <!-- AI Model Settings -->
        <div class="mb-8 border-b pb-8">
          <h2 class="text-xl font-semibold text-gray-700 mb-4">AI 模型設定</h2>
          
          <!-- Ollama URL -->
          <div class="mb-6">
            <label for="ollama-url" class="block text-gray-700 text-sm font-bold mb-2">
              Ollama 服務 URL
            </label>
            <div class="flex items-center space-x-2">
              <input
                type="text"
                id="ollama-url"
                v-model="form.ollama_url"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="例如: http://localhost:11434"
              />
              <button
                type="button"
                @click="testConnection"
                :disabled="isTestingConnection"
                class="px-4 py-2 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 disabled:bg-gray-400 whitespace-nowrap"
              >
                {{ isTestingConnection ? '測試中...' : '測試連線' }}
              </button>
            </div>
            <p v-if="testConnectionStatus" :class="testConnectionStatus.isError ? 'text-red-500' : 'text-green-500'" class="text-xs mt-2">
              {{ testConnectionStatus.message }}
            </p>
          </div>

          <!-- Ollama Model Selection -->
          <div class="mb-6">
            <label for="ollama-model" class="block text-gray-700 text-sm font-bold mb-2">
              Ollama 模型
            </label>
            <p class="text-xs text-gray-500 mb-2">
              從 Ollama 服務選擇一個模型用於自動再生。
            </p>
            <div class="flex items-center space-x-2">
              <select
                id="ollama-model"
                v-model="form.ollama_model"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              >
                <option v-if="ollamaModels.length === 0" value="" disabled>請先確認 URL 並刷新</option>
                <option v-for="model in ollamaModels" :key="model.name" :value="model.name">
                  {{ model.name }}
                </option>
              </select>
              <button
                type="button"
                @click="fetchOllamaModels"
                class="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 whitespace-nowrap"
              >
                刷新列表
              </button>
            </div>
          </div>

          <!-- Pull Model -->
          <div class="mb-6">
            <label for="pull-model" class="block text-gray-700 text-sm font-bold mb-2">
              下載新模型
            </label>
            <div class="flex items-center space-x-2">
              <input
                type="text"
                id="pull-model"
                v-model="modelToPull"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="例如: llama3:latest"
              />
              <button
                type="button"
                @click="pullModel"
                :disabled="isPullingModel || !modelToPull"
                class="px-4 py-2 bg-teal-600 text-white font-semibold rounded-lg hover:bg-teal-700 disabled:bg-teal-400 whitespace-nowrap"
              >
                {{ isPullingModel ? '下載中...' : '下載' }}
              </button>
            </div>
            <div v-if="pullStatus" class="mt-2 text-sm text-gray-600 bg-gray-100 p-3 rounded">
              <pre class="whitespace-pre-wrap break-all">{{ pullStatus }}</pre>
            </div>
          </div>
        </div>

        <!-- Review Threshold -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold text-gray-700 mb-4">審核閾值設定</h2>
          <div class="mb-6">
            <label for="rejection-threshold" class="block text-gray-700 text-sm font-bold mb-2">
              拒絕閾值 (Rejection Threshold)
            </label>
            <p class="text-xs text-gray-500 mb-2">
              當一筆資料的拒絕數量達到此數值，將自動觸發重生成。
            </p>
            <input
              type="number"
              id="rejection-threshold"
              v-model.number="form.rejection_threshold"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              min="1"
            />
          </div>
        </div>

        <!-- Save Button -->
        <div class="mt-8 flex justify-end">
          <button
            type="submit"
            :disabled="isSaving"
            class="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:bg-blue-400"
          >
            {{ isSaving ? '儲存中...' : '儲存設定' }}
          </button>
        </div>
      </form>
      
      <div v-if="successMessage" class="mt-4 text-green-600 bg-green-100 p-3 rounded-lg text-center">
        {{ successMessage }}
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import useAuth from '../store/auth';

const { instance } = useAuth();

const form = ref({
  rejection_threshold: 3,
  ollama_model: 'llama3',
  ollama_url: '',
});
const loading = ref(true);
const isSaving = ref(false);
const error = ref(null);
const successMessage = ref('');

// New state for Ollama interactions
const isTestingConnection = ref(false);
const testConnectionStatus = ref(null); // { isError: boolean, message: string }
const ollamaModels = ref([]);
const modelToPull = ref('');
const isPullingModel = ref(false);
const pullStatus = ref('');


const fetchSettings = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await instance.get('/api/v1/settings/');
    form.value = response.data;
    // After getting settings, fetch the models from the configured URL
    await fetchOllamaModels();
  } catch (err) {
    error.value = '無法獲取系統設定。';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const saveSettings = async () => {
  isSaving.value = true;
  error.value = null;
  successMessage.value = '';
  try {
    await instance.put('/api/v1/settings/', { settings: form.value });
    successMessage.value = '設定已成功儲存！';
    setTimeout(() => successMessage.value = '', 3000);
  } catch (err) {
    error.value = '儲存設定失敗。';
    console.error(err);
  } finally {
    isSaving.value = false;
  }
};

const testConnection = async () => {
  if (!form.value.ollama_url) {
    testConnectionStatus.value = { isError: true, message: '請輸入 Ollama URL。' };
    return;
  }
  isTestingConnection.value = true;
  testConnectionStatus.value = null;
  try {
    const response = await instance.post('/api/v1/ollama/test-connection', { url: form.value.ollama_url });
    testConnectionStatus.value = { isError: false, message: `連線成功！Ollama 版本: ${response.data.version}` };
  } catch (err) {
    const detail = err.response?.data?.detail || '未知錯誤';
    testConnectionStatus.value = { isError: true, message: `連線失敗: ${detail}` };
    console.error(err);
  } finally {
    isTestingConnection.value = false;
  }
};

const fetchOllamaModels = async () => {
  ollamaModels.value = [];
  try {
    const response = await instance.get('/api/v1/ollama/models');
    ollamaModels.value = response.data;
    if (response.data.length === 0) {
      // Maybe show a small warning if no models are found
    }
  } catch (err) {
    console.error('無法獲取 Ollama 模型列表:', err);
    // Do not show a big error, just log it. The dropdown will be empty.
  }
};

const pullModel = async () => {
  if (!modelToPull.value) return;
  isPullingModel.value = true;
  pullStatus.value = `正在開始下載 ${modelToPull.value}...`;
  
  // We must use the native fetch API for streaming responses in the browser,
  // as axios does not support it well.
  const token = localStorage.getItem('token');
  if (!token) {
    pullStatus.value = "錯誤：未授權。請重新登入。";
    isPullingModel.value = false;
    return;
  }

  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/v1/ollama/pull`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ model_name: modelToPull.value }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `伺服器錯誤 ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    let buffer = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        pullStatus.value += '\n\n下載完成！';
        break;
      }
      
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      
      for (let i = 0; i < lines.length - 1; i++) {
        const line = lines[i];
        if (line.trim() === '') continue;
        try {
          const progress = JSON.parse(line);
          let status_text = progress.status;
          if (progress.digest) {
              status_text += ` (layer: ${progress.digest.substring(7, 19)})`;
          }
          if (progress.total && progress.completed) {
              const percent = Math.round((progress.completed / progress.total) * 100);
              status_text += ` - ${percent}%`;
          }
          pullStatus.value = status_text;
        } catch (e) {
            console.warn("Could not parse stream line as JSON: ", line);
            pullStatus.value = line;
        }
      }
      buffer = lines[lines.length - 1];
    }
    
    await fetchOllamaModels(); // Refresh the list after pulling
    modelToPull.value = ''; // Clear input

  } catch (err) {
    pullStatus.value = `下載失敗: ${err.message}`;
    console.error(err);
  } finally {
    isPullingModel.value = false;
    setTimeout(() => {
        if (pullStatus.value.includes('下載完成')) {
            pullStatus.value = '';
        }
    }, 5000);
  }
};

onMounted(fetchSettings);
</script> 