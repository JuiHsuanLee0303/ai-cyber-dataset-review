import { reactive, readonly } from 'vue'
import axios from 'axios'

// 動態獲取 API URL
const getApiUrl = () => {
  // 如果設置了環境變數，使用環境變數
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }

  return 'http://localhost:8000'
}

const API_URL = getApiUrl()
console.log('API URL:', API_URL)

const state = reactive({
  isLoggedIn: false,
  user: null, // { username: '...', role: '...' }
  accessToken: localStorage.getItem('accessToken') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  isRefreshing: false,
  refreshPromise: null,
})

const instance = axios.create({
  baseURL: API_URL,
  timeout: 10000, // 10 秒超時
})

// 添加請求攔截器來處理錯誤
instance.interceptors.request.use(
  (config) => {
    // 添加請求日誌
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    // 添加 ngrok-skip-browser-warning header
    config.headers['ngrok-skip-browser-warning'] = '69420'
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 添加響應攔截器來處理錯誤
instance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('Response error:', error)
    
    // 檢查是否是 ngrok 錯誤頁面
    if (error.response?.data && typeof error.response.data === 'string' && 
        error.response.data.includes('<!DOCTYPE html>')) {
      console.error('Received HTML instead of JSON - possible ngrok/proxy issue')
      return Promise.reject(new Error('API 服務不可用，請檢查網路連接或服務狀態'))
    }
    
    return Promise.reject(error)
  }
)

// Function to refresh token
const refreshToken = async () => {
  if (state.isRefreshing) {
    // If already refreshing, wait for the existing promise
    return state.refreshPromise
  }

  if (!state.refreshToken) {
    throw new Error('No refresh token available')
  }

  state.isRefreshing = true
  state.refreshPromise = new Promise(async (resolve, reject) => {
    try {
      const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
        refresh_token: state.refreshToken,
      })
      
      const { access_token, refresh_token } = response.data
      
      state.accessToken = access_token
      state.refreshToken = refresh_token
      localStorage.setItem('accessToken', access_token)
      localStorage.setItem('refreshToken', refresh_token)
      
      // Update user info from new token
      const payload = JSON.parse(atob(access_token.split('.')[1]))
      const user = { username: payload.sub, role: payload.role }
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
      
      resolve({ access_token, refresh_token })
    } catch (error) {
      console.error('Token refresh failed:', error)
      logout()
      reject(error)
    } finally {
      state.isRefreshing = false
      state.refreshPromise = null
    }
  })

  return state.refreshPromise
}

// Request interceptor to refresh token before each request
instance.interceptors.request.use(async (config) => {
  // Skip token refresh for auth endpoints to avoid infinite loops
  if (config.url && (config.url.includes('/auth/token') || config.url.includes('/auth/refresh'))) {
    return config
  }

  // If we have a refresh token, try to refresh before making the request
  if (state.refreshToken && !state.isRefreshing) {
    try {
      await refreshToken()
    } catch (error) {
      // If refresh fails, the request will fail with 401 and be handled by response interceptor
      console.warn('Pre-request token refresh failed:', error)
    }
  }

  if (state.accessToken) {
    config.headers.Authorization = `Bearer ${state.accessToken}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// Response interceptor for handling 401 errors
instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        await refreshToken()
        originalRequest.headers.Authorization = `Bearer ${state.accessToken}`
        return instance(originalRequest)
      } catch (refreshError) {
        console.error('Response interceptor refresh failed:', refreshError)
        logout()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)


const login = async (username, password) => {
  try {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)

    const response = await instance.post('/api/v1/auth/token', params)
    
    const { access_token, refresh_token } = response.data;
    state.accessToken = access_token;
    state.refreshToken = refresh_token;
    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);
    
    // Decode token to get user info
    const payload = JSON.parse(atob(access_token.split('.')[1]))
    const user = { username: payload.sub, role: payload.role }
    state.user = user
    localStorage.setItem('user', JSON.stringify(user))

    state.isLoggedIn = true
    return true
  } catch (error) {
    console.error('Login failed:', error)
    logout()
    return false
  }
}

const logout = () => {
  state.isLoggedIn = false
  state.user = null
  state.accessToken = null
  state.refreshToken = null
  state.isRefreshing = false
  state.refreshPromise = null
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('user')
}

const checkAuthState = () => {
  const token = localStorage.getItem('accessToken')
  const user = localStorage.getItem('user')
  if (token && user) {
    state.accessToken = token
    state.user = JSON.parse(user)
    state.isLoggedIn = true
  }
}

// Check auth state when the app loads
checkAuthState()

export default function useAuth() {
  return {
    state: readonly(state),
    login,
    logout,
    refreshToken, // Export refresh function for manual refresh
    instance, // Export axios instance to be used in other parts of the app
  }
}
