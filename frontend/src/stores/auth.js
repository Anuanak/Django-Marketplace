import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/authService'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const loading = ref(false)
  
  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const userType = computed(() => user.value?.user_type)
  const isSeller = computed(() => userType.value === 'seller')
  const isBuyer = computed(() => userType.value === 'buyer')
  const isAdmin = computed(() => userType.value === 'admin')
  const balance = computed(() => user.value?.balance || '0.00')
  
  // Actions
  async function login(credentials) {
    try {
      loading.value = true
      const response = await authService.login(credentials)
      
      user.value = response.data.user
      token.value = response.data.tokens.access
      refreshToken.value = response.data.tokens.refresh
      
      localStorage.setItem('access_token', token.value)
      localStorage.setItem('refresh_token', refreshToken.value)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Login failed' 
      }
    } finally {
      loading.value = false
    }
  }
  
  async function register(userData) {
    try {
      loading.value = true
      const response = await authService.register(userData)
      
      user.value = response.data.user
      token.value = response.data.tokens.access
      refreshToken.value = response.data.tokens.refresh
      
      localStorage.setItem('access_token', token.value)
      localStorage.setItem('refresh_token', refreshToken.value)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Registration failed' 
      }
    } finally {
      loading.value = false
    }
  }
  
  async function logout() {
    try {
      if (refreshToken.value) {
        await authService.logout(refreshToken.value)
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      user.value = null
      token.value = null
      refreshToken.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }
  
  async function fetchProfile() {
    try {
      const response = await authService.getProfile()
      user.value = response.data
      return { success: true }
    } catch (error) {
      return { success: false }
    }
  }
  
  async function refreshAccessToken() {
    try {
      if (!refreshToken.value) return false
      
      const response = await authService.refreshToken(refreshToken.value)
      token.value = response.data.access
      
      localStorage.setItem('access_token', token.value)
      
      if (response.data.refresh) {
        refreshToken.value = response.data.refresh
        localStorage.setItem('refresh_token', refreshToken.value)
      }
      
      return true
    } catch (error) {
      logout()
      return false
    }
  }
  
  async function updateBalance() {
    try {
      const response = await authService.getBalance()
      if (user.value) {
        user.value.balance = response.data.balance
      }
    } catch (error) {
      console.error('Failed to update balance:', error)
    }
  }
  
  // Initialize auth state
  if (token.value) {
    fetchProfile()
  }
  
  return {
    user,
    token,
    loading,
    isAuthenticated,
    userType,
    isSeller,
    isBuyer,
    isAdmin,
    balance,
    login,
    register,
    logout,
    fetchProfile,
    refreshToken: refreshAccessToken,
    updateBalance
  }
})
