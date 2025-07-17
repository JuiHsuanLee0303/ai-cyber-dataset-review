<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-800 mb-6">法規條文管理</h1>

    <!-- Import Section -->
    <div class="bg-white p-6 rounded-lg shadow-md mb-8">
      <h2 class="text-xl font-semibold mb-4">匯入法規</h2>
      <p class="text-sm text-gray-600 mb-4">
        請在此貼上單筆 JSON 物件或多筆 JSON 物件組成的陣列。範例格式：<br>
        <code>[{"title": "法規標題", "number": "條號", "content": "法規內容"}, ...]</code>
      </p>
      <textarea
        v-model="jsonInput"
        rows="10"
        class="w-full p-2 border rounded-md font-mono text-sm"
        placeholder='[{"title": "資通安全管理法", "number": "1", "content": "..."}]'
      ></textarea>
      <div v-if="importError" class="text-red-500 text-sm mt-2">{{ importError }}</div>
      <div class="mt-4 text-right">
        <button
          @click="handleImport"
          :disabled="importing"
          class="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-blue-300"
        >
          {{ importing ? '匯入中...' : '匯入' }}
        </button>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-2xl">
        <h3 class="text-xl font-bold mb-4">編輯法規</h3>
        <form @submit.prevent="handleUpdate" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">標題</label>
            <input type="text" v-model="editingForm.title" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3" required>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">條號</label>
            <input type="text" v-model="editingForm.number" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3" required>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">內容</label>
            <textarea v-model="editingForm.content" rows="6" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3" required></textarea>
          </div>
          <div class="mt-6 flex justify-end space-x-4">
            <button type="button" @click="closeEditModal" class="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400">取消</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">確認更新</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Articles Table -->
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <h2 class="text-xl font-semibold p-6">已匯入法規列表</h2>
      <table class="min-w-full leading-normal">
        <thead>
          <tr>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">ID</th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">標題</th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">條號</th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">內容</th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="5" class="text-center py-10">載入中...</td></tr>
          <tr v-else-if="articles.length === 0"><td colspan="5" class="text-center py-10">沒有資料。</td></tr>
          <tr v-else v-for="item in articles" :key="item.id">
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">{{ item.id }}</td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">{{ item.title }}</td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">{{ item.number }}</td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm"><p class="truncate max-w-lg">{{ item.content }}</p></td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
              <button @click="openEditModal(item)" class="text-indigo-600 hover:text-indigo-900 mr-4">編輯</button>
              <button @click="handleDelete(item.id)" class="text-red-600 hover:text-red-900">刪除</button>
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

// For Edit Modal
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

const handleImport = async () => {
  importError.value = ''
  if (!jsonInput.value.trim()) {
    importError.value = '輸入框不可為空。'
    return
  }

  let payload
  try {
    const parsed = JSON.parse(jsonInput.value)
    // Ensure payload is an array
    payload = Array.isArray(parsed) ? parsed : [parsed]
  } catch (error) {
    importError.value = 'JSON 格式錯誤，請檢查您的輸入。'
    return
  }

  importing.value = true
  try {
    await instance.post('/api/v1/legal-articles/', payload)
    jsonInput.value = '' // Clear input on success
    await fetchArticles() // Refresh the list
    toast.success('匯入成功！')
  } catch (error) {
    console.error('Failed to import articles:', error)
    importError.value = `匯入失敗: ${error.response?.data?.detail || '未知錯誤'}`
  } finally {
    importing.value = false
  }
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