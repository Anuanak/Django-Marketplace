import api from './api'

export default {
  // Create order
  createOrder(orderData) {
    return api.post('/orders/', orderData)
  },
  
  // Get user orders
  getOrders(params) {
    return api.get('/orders/', { params })
  },
  
  // Get single order
  getOrder(id) {
    return api.get(`/orders/${id}/`)
  },
  
  // Cancel order
  cancelOrder(id) {
    return api.post(`/orders/${id}/cancel/`)
  },
  
  // Get seller orders (for sellers)
  getSellerOrders(params) {
    return api.get('/orders/seller/', { params })
  }
}
