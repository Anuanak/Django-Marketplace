import { defineStore } from 'pinia'
import { ref } from 'vue'
import productService from '@/services/productService'

export const useProductStore = defineStore('product', () => {
  // State
  const products = ref([])
  const currentProduct = ref(null)
  const categories = ref([])
  const filters = ref({
    search: '',
    category: null,
    min_price: null,
    max_price: null,
    product_type: null,
    ordering: '-created_at'
  })
  const pagination = ref({
    page: 1,
    page_size: 20,
    count: 0
  })
  const loading = ref(false)
  
  // Actions
  async function fetchProducts(newFilters = {}) {
    try {
      loading.value = true
      const params = {
        ...filters.value,
        ...newFilters,
        page: pagination.value.page,
        page_size: pagination.value.page_size
      }
      
      const response = await productService.getProducts(params)
      products.value = response.data.results
      pagination.value.count = response.data.count
      
      return { success: true }
    } catch (error) {
      console.error('Failed to fetch products:', error)
      return { success: false }
    } finally {
      loading.value = false
    }
  }
  
  async function fetchProduct(slug) {
    try {
      loading.value = true
      const response = await productService.getProduct(slug)
      currentProduct.value = response.data
      return { success: true }
    } catch (error) {
      console.error('Failed to fetch product:', error)
      return { success: false }
    } finally {
      loading.value = false
    }
  }
  
  async function fetchCategories() {
    try {
      const response = await productService.getCategories()
      categories.value = response.data.results || response.data
      return { success: true }
    } catch (error) {
      console.error('Failed to fetch categories:', error)
      return { success: false }
    }
  }
  
  function updateFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1
  }
  
  function setPage(page) {
    pagination.value.page = page
  }
  
  return {
    products,
    currentProduct,
    categories,
    filters,
    pagination,
    loading,
    fetchProducts,
    fetchProduct,
    fetchCategories,
    updateFilters,
    setPage
  }
})
