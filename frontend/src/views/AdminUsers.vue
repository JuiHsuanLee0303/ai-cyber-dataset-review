<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">使用者管理</h1>
      <button @click="openAddModal" class="px-4 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700">
        新增使用者
      </button>
    </div>

    <!-- Users Table -->
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full leading-normal">
        <thead>
          <tr>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              使用者名稱
            </th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              角色
            </th>
            <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="3" class="text-center py-10">載入中...</td>
          </tr>
          <tr v-else v-for="user in users" :key="user.id">
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              <p class="text-gray-900 whitespace-no-wrap">{{ user.username }}</p>
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              <span 
                :class="user.role === 'admin' ? 'bg-indigo-200 text-indigo-800' : 'bg-gray-200 text-gray-800'"
                class="px-2 py-1 font-semibold leading-tight rounded-full text-xs"
              >
                {{ user.role === 'admin' ? '系統管理員' : '資安專家' }}
              </span>
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
              <button @click="openEditModal(user)" class="text-indigo-600 hover:text-indigo-900 mr-4 disabled:opacity-50" :disabled="user.username === 'admin'">編輯</button>
              <button @click="handleDeleteUser(user)" class="text-red-600 hover:text-red-900 disabled:opacity-50" :disabled="user.username === 'admin'">刪除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add User Modal -->
    <div v-if="showAddUserModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">新增使用者</h3>
        <form @submit.prevent="handleCreateUser">
          <div class="mb-4">
            <label for="username" class="block text-sm font-medium text-gray-700">帳號</label>
            <input v-model="newUser.username" type="text" id="username" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" required>
          </div>
          <div class="mb-4">
            <label for="password" class="block text-sm font-medium text-gray-700">密碼</label>
            <input v-model="newUser.password" type="password" id="password" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" required>
          </div>
          <div class="mb-6">
            <label for="role" class="block text-sm font-medium text-gray-700">角色</label>
            <select v-model="newUser.role" id="role" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
              <option value="expert">資安專家</option>
              <option value="admin">系統管理員</option>
            </select>
          </div>
           <div v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</div>
          <div class="mt-6 flex justify-end space-x-4">
            <button type="button" @click="showAddUserModal = false" class="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400">取消</button>
            <button type="submit" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">確認新增</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit User Modal -->
    <div v-if="showEditUserModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">編輯使用者</h3>
        <form @submit.prevent="handleUpdateUser">
          <div class="mb-4">
            <label for="edit-username" class="block text-sm font-medium text-gray-700">帳號</label>
            <input v-model="editingUser.username" type="text" id="edit-username" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 bg-gray-100" readonly>
          </div>
          <div class="mb-4">
            <label for="edit-password" class="block text-sm font-medium text-gray-700">新密碼 (可選)</label>
            <input v-model="editingUser.password" type="password" id="edit-password" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
          </div>
          <div class="mb-6">
            <label for="edit-role" class="block text-sm font-medium text-gray-700">角色</label>
            <select v-model="editingUser.role" id="edit-role" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
              <option value="expert">資安專家</option>
              <option value="admin">系統管理員</option>
            </select>
          </div>
           <div v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</div>
          <div class="mt-6 flex justify-end space-x-4">
            <button type="button" @click="showEditUserModal = false" class="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400">取消</button>
            <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">確認更新</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useAuth from '../store/auth'

const { instance } = useAuth()

const users = ref([])
const loading = ref(true)
const error = ref(null)

const showAddUserModal = ref(false)
const newUser = ref({
  username: '',
  password: '',
  role: 'expert'
})

const showEditUserModal = ref(false)
const editingUser = ref(null)

const fetchUsers = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await instance.get('/api/v1/users/')
    users.value = response.data
  } catch (err) {
    error.value = '無法獲取使用者列表。'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const openAddModal = () => {
  error.value = null
  newUser.value = { username: '', password: '', role: 'expert' }
  showAddUserModal.value = true
}

const openEditModal = (user) => {
  error.value = null
  // Create a copy to avoid modifying the original object directly
  editingUser.value = { ...user, password: '' } 
  showEditUserModal.value = true
}

const handleCreateUser = async () => {
  error.value = null
  try {
    await instance.post('/api/v1/users/', newUser.value)
    showAddUserModal.value = false
    await fetchUsers() // Refresh the list
  } catch (err) {
    error.value = `新增使用者失敗: ${err.response?.data?.detail || '未知錯誤'}`
    console.error(err)
  }
}

const handleUpdateUser = async () => {
  if (!editingUser.value) return
  error.value = null

  // Create a payload with only the fields that should be updated
  const payload = {
    role: editingUser.value.role
  }
  if (editingUser.value.password) {
    payload.password = editingUser.value.password
  }

  try {
    await instance.put(`/api/v1/users/${editingUser.value.id}`, payload)
    showEditUserModal.value = false
    await fetchUsers() // Refresh the list
  } catch (err) {
    error.value = `更新使用者失敗: ${err.response?.data?.detail || '未知錯誤'}`
    console.error(err)
  }
}

const handleDeleteUser = async (user) => {
  if (confirm(`確定要刪除使用者 ${user.username} 嗎？此操作無法復原。`)) {
    error.value = null
    try {
      await instance.delete(`/api/v1/users/${user.id}`)
      await fetchUsers() // Refresh the list
    } catch (err) {
      error.value = `刪除使用者失敗: ${err.response?.data?.detail || '未知錯誤'}`
      console.error(err)
    }
  }
}

onMounted(() => {
  fetchUsers()
})
</script> 