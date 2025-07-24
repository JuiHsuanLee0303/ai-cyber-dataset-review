<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">法規條文管理</h1>
      <button
        @click="openImportModal"
        class="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
        </svg>
        匯入法規
      </button>
    </div>

    <!-- Import Modal -->
    <div v-if="showImportModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold flex items-center">
            <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
            匯入法規
          </h2>
          <button @click="closeImportModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <!-- Import Tabs -->
        <div class="mb-6">
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8">
              <button
                @click="activeTab = 'text'"
                :class="[
                  'py-2 px-1 border-b-2 font-medium text-sm',
                  activeTab === 'text'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                文字輸入
              </button>
              <button
                @click="activeTab = 'file'"
                :class="[
                  'py-2 px-1 border-b-2 font-medium text-sm',
                  activeTab === 'file'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"></path>
                </svg>
                檔案上傳
              </button>
            </nav>
          </div>
        </div>

        <!-- Text Input Tab -->
        <div v-if="activeTab === 'text'" class="space-y-4">
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-blue-800">格式說明</h3>
                <div class="mt-2 text-sm text-blue-700">
                  <p>請在此貼上單筆 JSON 物件或多筆 JSON 物件組成的陣列。</p>
                  <p class="mt-1">範例格式：</p>
                  <code class="block mt-2 bg-blue-100 p-2 rounded text-xs">
                    [{"title": "法規標題", "number": "條號", "content": "法規內容"}, ...]
                  </code>
                </div>
              </div>
            </div>
          </div>
          
          <textarea
            v-model="jsonInput"
            rows="12"
            class="w-full p-3 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder='[{"title": "資通安全管理法", "number": "1", "content": "為維護國家資通安全..."}]'
          ></textarea>
          
          <div v-if="importError" class="bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-red-700">{{ importError }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- File Upload Tab -->
        <div v-if="activeTab === 'file'" class="space-y-4">
          <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-green-800">檔案上傳說明</h3>
                <div class="mt-2 text-sm text-green-700">
                  <p>支援 JSON 檔案格式，檔案內容應為法規條文的陣列。</p>
                  <p class="mt-1">檔案大小限制：5MB</p>
                </div>
              </div>
            </div>
          </div>

          <!-- File Upload Area -->
          <div
            @drop.prevent="handleFileDrop"
            @dragover.prevent="dragOver = true"
            @dragleave.prevent="dragOver = false"
            :class="[
              'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
              dragOver
                ? 'border-blue-400 bg-blue-50'
                : 'border-gray-300 hover:border-gray-400'
            ]"
          >
            <div v-if="!selectedFile">
              <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <div class="mt-4">
                <label for="file-upload" class="cursor-pointer">
                  <span class="mt-2 block text-sm font-medium text-gray-900">
                    拖放檔案至此處，或
                    <span class="text-blue-600 hover:text-blue-500">點擊選擇檔案</span>
                  </span>
                  <span class="mt-1 block text-xs text-gray-500">JSON 檔案</span>
                </label>
                <input
                  id="file-upload"
                  ref="fileInput"
                  type="file"
                  accept=".json"
                  class="sr-only"
                  @change="handleFileSelect"
                />
              </div>
            </div>
            
            <div v-else class="space-y-4">
              <div class="flex items-center justify-center">
                <svg class="h-8 w-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">{{ selectedFile.name }}</p>
                <p class="text-xs text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
              </div>
              <button
                @click="clearSelectedFile"
                class="text-sm text-red-600 hover:text-red-500"
              >
                移除檔案
              </button>
            </div>
          </div>

          <div v-if="fileError" class="bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-red-700">{{ fileError }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Import Button -->
        <div class="mt-6 flex justify-end space-x-3">
          <button
            @click="closeImportModal"
            class="px-4 py-2 text-gray-700 bg-gray-100 font-medium rounded-lg hover:bg-gray-200 transition-colors"
          >
            取消
          </button>
          <button
            v-if="activeTab === 'file' && selectedFile"
            @click="clearSelectedFile"
            class="px-4 py-2 text-gray-700 bg-gray-100 font-medium rounded-lg hover:bg-gray-200 transition-colors"
          >
            清除
          </button>
          <button
            @click="handleImport"
            :disabled="importing || (activeTab === 'text' && !jsonInput.trim()) || (activeTab === 'file' && !selectedFile)"
            class="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors flex items-center"
          >
            <svg v-if="importing" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ importing ? '匯入中...' : '匯入' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">編輯法規</h3>
          <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleUpdate" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">標題</label>
            <input 
              type="text" 
              v-model="editingForm.title" 
              class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
              required
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">條號</label>
            <input 
              type="text" 
              v-model="editingForm.number" 
              class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
              required
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">內容</label>
            <textarea 
              v-model="editingForm.content" 
              rows="6" 
              class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
              required
            ></textarea>
          </div>
          <div class="mt-6 flex justify-end space-x-4">
            <button 
              type="button" 
              @click="closeEditModal" 
              class="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400 transition-colors"
            >
              取消
            </button>
            <button 
              type="submit" 
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              確認更新
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Articles Table -->
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <h2 class="text-xl font-semibold flex items-center">
            <svg class="w-5 h-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            已匯入法規列表
            <span class="ml-2 text-sm text-gray-500">({{ filteredArticles.length }} 筆)</span>
          </h2>
          
          <!-- 篩選區域 -->
          <div class="flex flex-col sm:flex-row gap-3">
            <!-- 標題篩選 -->
            <div class="relative">
              <input
                type="text"
                v-model="titleFilter"
                placeholder="搜尋法規標題... (按 Enter 快速搜尋)"
                @keyup.enter="handleSearch"
                class="w-full sm:w-64 px-4 py-2 pl-10 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              />
              <svg class="absolute left-3 top-2.5 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            
            <!-- 清除篩選按鈕 -->
            <button
              v-if="titleFilter"
              @click="clearFilters"
              class="px-3 py-2 text-sm text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors flex items-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
              清除篩選
            </button>
          </div>
        </div>
        
        <!-- 篩選統計資訊 -->
        <div v-if="titleFilter" class="mt-3 flex items-center text-sm text-gray-600">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          搜尋標題包含 "{{ titleFilter }}" 的結果：{{ filteredArticles.length }} 筆
          <span v-if="filteredArticles.length !== articles.length" class="ml-2 text-gray-500">
            (共 {{ articles.length }} 筆)
          </span>
          <span v-if="filteredArticles.length > 0" class="ml-2 text-green-600">
            ✓ 找到 {{ filteredArticles.length }} 筆符合的結果
          </span>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">標題</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">條號</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">內容</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="5" class="px-6 py-12 text-center">
                <div class="flex items-center justify-center">
                  <svg class="animate-spin h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span class="ml-2 text-gray-600">載入中...</span>
                </div>
              </td>
            </tr>
            <tr v-else-if="articles.length === 0">
              <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <p class="mt-2">沒有資料</p>
              </td>
            </tr>
            <tr v-else-if="titleFilter && filteredArticles.length === 0">
              <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
                <p class="mt-2">找不到符合 "{{ titleFilter }}" 的法規</p>
                <p class="mt-1 text-sm text-gray-400">請嘗試其他關鍵字或清除篩選</p>
              </td>
            </tr>
            <tr v-else v-for="item in filteredArticles" :key="item.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <span v-if="titleFilter" v-html="highlightText(item.title, titleFilter)"></span>
                <span v-else>{{ item.title }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">{{ item.number }}</td>
              <td class="px-6 py-4 text-sm text-gray-900">
                <p class="truncate max-w-lg">{{ item.content.substring(0, 25) }} {{item.content.length > 30 ? '...' : ''}}</p>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                <button 
                  @click="openEditModal(item)" 
                  class="text-indigo-600 hover:text-indigo-900 mr-4 transition-colors"
                >
                  編輯
                </button>
                <button 
                  @click="handleDelete(item.id)" 
                  class="text-red-600 hover:text-red-900 transition-colors"
                >
                  刪除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'
import useConfirm from '../composables/useConfirm'

const { instance } = useAuth()
const toast = useToast()
const { confirm } = useConfirm()

const articles = ref([])
const loading = ref(true)
const jsonInput = ref('')
const importError = ref('')
const importing = ref(false)

// 篩選相關
const titleFilter = ref('')

// 篩選後的資料
const filteredArticles = computed(() => {
  if (!titleFilter.value.trim()) {
    return articles.value
  }
  
  const filterText = titleFilter.value.toLowerCase().trim()
  return articles.value.filter(article => 
    article.title.toLowerCase().includes(filterText)
  )
})

// Tab management
const activeTab = ref('text')

// File upload
const selectedFile = ref(null)
const fileError = ref('')
const dragOver = ref(false)
const fileInput = ref(null)

// Modal management
const showImportModal = ref(false)
const showEditModal = ref(false)
const editingArticle = ref(null)
const editingForm = ref({ id: null, title: '', number: '', content: '' })

const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await instance.get('/api/v1/legal-articles/')
    articles.value = response.data
  } catch (error) {
    console.error('Failed to load articles:', error)
    toast.error('載入法規列表失敗。')
  } finally {
    loading.value = false
  }
}

// 清除篩選
const clearFilters = () => {
  titleFilter.value = ''
}

// 高亮匹配的文字
const highlightText = (text, searchText) => {
  if (!searchText.trim()) {
    return text
  }
  
  const regex = new RegExp(`(${searchText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
  return text.replace(regex, '<mark class="bg-yellow-200 px-1 rounded">$1</mark>')
}

// 處理搜尋
const handleSearch = () => {
  // 這裡可以添加額外的搜尋邏輯，比如記錄搜尋歷史等
  console.log('搜尋:', titleFilter.value)
}

const openImportModal = () => {
  showImportModal.value = true
  // Reset form when opening
  activeTab.value = 'text'
  jsonInput.value = ''
  importError.value = ''
  clearSelectedFile()
}

const closeImportModal = () => {
  showImportModal.value = false
  // Reset form when closing
  jsonInput.value = ''
  importError.value = ''
  clearSelectedFile()
}

const handleImport = async () => {
  importError.value = ''
  fileError.value = ''
  
  if (activeTab.value === 'text') {
    if (!jsonInput.value.trim()) {
      importError.value = '輸入框不可為空。'
      return
    }
    
    let payload
    try {
      const parsed = JSON.parse(jsonInput.value)
      payload = Array.isArray(parsed) ? parsed : [parsed]
    } catch (error) {
      importError.value = 'JSON 格式錯誤，請檢查您的輸入。'
      return
    }
    
    await performImport(payload)
    jsonInput.value = '' // Clear input on success
  } else if (activeTab.value === 'file') {
    if (!selectedFile.value) {
      fileError.value = '請選擇檔案。'
      return
    }
    
    try {
      const content = await readFileContent(selectedFile.value)
      const parsed = JSON.parse(content)
      const payload = Array.isArray(parsed) ? parsed : [parsed]
      
      await performImport(payload)
      clearSelectedFile() // Clear file on success
    } catch (error) {
      fileError.value = '檔案讀取失敗或JSON格式錯誤。'
      console.error('File import error:', error)
    }
  }
}

const performImport = async (payload) => {
  importing.value = true
  try {
    await instance.post('/api/v1/legal-articles/', payload)
    await fetchArticles() // Refresh the list
    toast.success(`成功匯入 ${payload.length} 筆法規！`)
    closeImportModal() // Close modal on success
  } catch (error) {
    console.error('Failed to import articles:', error)
    const errorMessage = error.response?.data?.detail || '未知錯誤'
    if (activeTab.value === 'text') {
      importError.value = `匯入失敗: ${errorMessage}`
    } else {
      fileError.value = `匯入失敗: ${errorMessage}`
    }
  } finally {
    importing.value = false
  }
}

const readFileContent = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.onerror = reject
    reader.readAsText(file)
  })
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const handleFileDrop = (event) => {
  dragOver.value = false
  const file = event.dataTransfer.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const validateAndSetFile = (file) => {
  fileError.value = ''
  
  // Check file type
  if (file.type !== 'application/json' && !file.name.endsWith('.json')) {
    fileError.value = '請選擇 JSON 檔案。'
    return
  }
  
  // Check file size (5MB limit)
  if (file.size > 5 * 1024 * 1024) {
    fileError.value = '檔案大小不能超過 5MB。'
    return
  }
  
  selectedFile.value = file
}

const clearSelectedFile = () => {
  selectedFile.value = null
  fileError.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const openEditModal = (article) => {
  editingArticle.value = article
  editingForm.value = { ...article }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingArticle.value = null
}

const handleUpdate = async () => {
  if (!editingArticle.value) return;
  try {
    await instance.put(`/api/v1/legal-articles/${editingArticle.value.id}`, editingForm.value)
    closeEditModal()
    await fetchArticles()
    toast.success('更新成功！')
  } catch (error) {
    console.error('Failed to update article:', error)
    toast.error(`更新失敗: ${error.response?.data?.detail || '未知錯誤'}`)
  }
}

const handleDelete = async (articleId) => {
  const confirmed = await confirm('刪除確認', '確定要刪除這條法規嗎？此操作無法復原。')
  if (!confirmed) return
  
  try {
    await instance.delete(`/api/v1/legal-articles/${articleId}`)
    await fetchArticles()
    toast.success('刪除成功！')
  } catch (error) {
    console.error('Failed to delete article:', error)
    toast.error(`刪除失敗: ${error.response?.data?.detail || '未知錯誤'}`)
  }
}

onMounted(fetchArticles)
</script> 