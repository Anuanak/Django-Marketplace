import api from './api'

export default {
  // Get balance
  getBalance() {
    return api.get('/payments/balance/')
  },
  
  // Top-up balance
  topUpBalance(amount, paymentMethod) {
    return api.post('/payments/topup/', {
      amount,
      payment_method: paymentMethod
    })
  },
  
  // Get transaction history
  getTransactions(params) {
    return api.get('/payments/transactions/', { params })
  },
  
  // Pay with balance
  payWithBalance(orderId) {
    return api.post(`/orders/${orderId}/pay-with-balance/`)
  }
}
