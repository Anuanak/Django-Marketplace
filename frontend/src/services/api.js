import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor - add auth token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors and token refresh
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    // Handle 401 Unauthorized - try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const authStore = useAuthStore()
      const refreshSuccessful = await authStore.refreshToken()
      
      if (refreshSuccessful) {
        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${authStore.token}`
        return api(originalRequest)
      } else {
        // Refresh failed, logout user
        authStore.logout()
        router.push({ name: 'login' })
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
