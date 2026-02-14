import api from './api'

export default {
  // Authentication
  login(credentials) {
    return api.post('/auth/login/', credentials)
  },
  
  register(userData) {
    return api.post('/auth/register/', userData)
  },
  
  logout(refreshToken) {
    return api.post('/auth/logout/', { refresh: refreshToken })
  },
  
  refreshToken(refreshToken) {
    return api.post('/auth/token/refresh/', { refresh: refreshToken })
  },
  
  // User profile
  getProfile() {
    return api.get('/auth/users/me/')
  },
  
  updateProfile(data) {
    return api.patch('/auth/users/me/', data)
  },
  
  changePassword(data) {
    return api.post('/auth/change-password/', data)
  },
  
  // Balance
  getBalance() {
    return api.get('/auth/users/balance/')
  }
}
