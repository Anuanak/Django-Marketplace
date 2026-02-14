import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import cartService from '@/services/cartService'
import { ElMessage } from 'element-plus'

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref([])
  const loading = ref(false)
  
  // Getters
  const totalItems = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })
  
  const totalPrice = computed(() => {
    return items.value.reduce((sum, item) => sum + (item.unit_price * item.quantity), 0)
  })
  
  const isEmpty = computed(() => items.value.length === 0)
  
  // Actions
  async function fetchCart() {
    try {
      loading.value = true
      const response = await cartService.getCart()
      items.value = response.data.items || []
    } catch (error) {
      console.error('Failed to fetch cart:', error)
      items.value = []
    } finally {
      loading.value = false
    }
  }
  
  async function addItem(productId, quantity = 1, variantId = null) {
    try {
      const response = await cartService.addToCart(productId, quantity, variantId)
      items.value = response.data.items
      ElMessage.success('Added to cart')
      return { success: true }
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || 'Failed to add to cart')
      return { success: false }
    }
  }
  
  async function updateItem(itemId, quantity) {
    try {
      await cartService.updateCartItem(itemId, quantity)
      const item = items.value.find(i => i.id === itemId)
      if (item) {
        item.quantity = quantity
      }
      return { success: true }
    } catch (error) {
      ElMessage.error('Failed to update cart item')
      return { success: false }
    }
  }
  
  async function removeItem(itemId) {
    try {
      await cartService.removeFromCart(itemId)
      items.value = items.value.filter(item => item.id !== itemId)
      ElMessage.success('Removed from cart')
      return { success: true }
    } catch (error) {
      ElMessage.error('Failed to remove item')
      return { success: false }
    }
  }
  
  async function clearCart() {
    try {
      await cartService.clearCart()
      items.value = []
      ElMessage.success('Cart cleared')
      return { success: true }
    } catch (error) {
      ElMessage.error('Failed to clear cart')
      return { success: false }
    }
  }
  
  // Auto-fetch cart on store init if user is authenticated
  // This will be called when the store is first accessed
  
  return {
    items,
    loading,
    totalItems,
    totalPrice,
    isEmpty,
    fetchCart,
    addItem,
    updateItem,
    removeItem,
    clearCart
  }
})
