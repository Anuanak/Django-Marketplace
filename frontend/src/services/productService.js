import api from './api'

export default {
  // Get products with filters
  getProducts(params) {
    return api.get('/products/', { params })
  },
  
  // Get single product by slug
  getProduct(slug) {
    return api.get(`/products/${slug}/`)
  },
  
  // Create product (seller only)
  createProduct(data) {
    return api.post('/products/', data)
  },
  
  // Update product (seller only)
  updateProduct(slug, data) {
    return api.put(`/products/${slug}/`, data)
  },
  
  // Delete product (seller only)
  deleteProduct(slug) {
    return api.delete(`/products/${slug}/`)
  },
  
  // Upload product images
  uploadImages(productId, files) {
    const formData = new FormData()
    files.forEach((file, index) => {
      formData.append(`image_${index}`, file)
    })
    return api.post(`/products/${productId}/upload-images/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  // Categories
  getCategories() {
    return api.get('/products/categories/')
  },
  
  // Wishlist
  getWishlist() {
    return api.get('/products/wishlist/')
  },
  
  addToWishlist(productId) {
    return api.post('/products/wishlist/', { product: productId })
  },
  
  removeFromWishlist(id) {
    return api.delete(`/products/wishlist/${id}/`)
  },
  
  // Promo codes
  validatePromoCode(code) {
    return api.post('/products/promo-code/validate/', { code })
  }
}
