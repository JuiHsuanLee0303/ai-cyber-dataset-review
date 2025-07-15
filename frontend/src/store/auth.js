import { reactive, readonly } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const state = reactive({
  isLoggedIn: false,
  user: null, // { username: '...', role: '...' }
  token: null,
})

const instance = axios.create({
  baseURL: API_URL,
})

instance.interceptors.request.use(config => {
  if (state.token) {
    config.headers.Authorization = `Bearer ${state.token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})


const login = async (username, password) => {
  try {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)

    const response = await instance.post('/api/v1/auth/token', params)
    
    const token = response.data.access_token
    state.token = token
    localStorage.setItem('token', token)
    
    // Decode token to get user info
    const payload = JSON.parse(atob(token.split('.')[1]))
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
  state.token = null
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

const checkAuthState = () => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  if (token && user) {
    state.token = token
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
    instance, // Export axios instance to be used in other parts of the app
  }
}
