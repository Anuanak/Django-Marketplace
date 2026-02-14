import api from './api'

export default {
  // Get current cart
  getCart() {
    return api.get('/cart/')
  },
  
  // Add item to cart
  addToCart(productId, quantity = 1, variantId = null) {
    return api.post('/cart/add/', {
      product: productId,
      quantity,
      variant: variantId
    })
  },
  
  // Update cart item quantity
  updateCartItem(itemId, quantity) {
    return api.patch(`/cart/items/${itemId}/`, { quantity })
  },
  
  // Remove item from cart
  removeFromCart(itemId) {
    return api.delete(`/cart/items/${itemId}/`)
  },
  
  // Clear entire cart
  clearCart() {
    return api.post('/cart/clear/')
  }
}
