import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const API = {
  // Products
  getProducts: (params?: any) => apiClient.get('/products/', { params }),
  getProduct: (id: string | number) => apiClient.get(`/products/${id}/`),
  getCategories: () => apiClient.get('/categories/'),
  
  // Cart
  getCart: () => apiClient.get('/cart/'),
  addToCart: (productId: number, quantity: number) =>
    apiClient.post('/cart/add_item/', { product_id: productId, quantity }),
  removeFromCart: (itemId: number) =>
    apiClient.post(`/cart/remove_item/`, { item_id: itemId }),
  updateCart: (itemId: number, quantity: number) =>
    apiClient.post(`/cart/update_item/`, { item_id: itemId, quantity }),
  
  // Orders
  getOrders: (params?: any) => apiClient.get('/orders/', { params }),
  getOrder: (id: string | number) => apiClient.get(`/orders/${id}/`),
  createOrder: (data: any) => apiClient.post('/orders/', data),
  
  // Reviews
  addReview: (productId: number, data: any) =>
    apiClient.post(`/products/${productId}/reviews/`, data),
  getReviews: (productId: number) =>
    apiClient.get(`/products/${productId}/reviews/`),
  
  // Auth
  login: (username: string, password: string) =>
    apiClient.post('/auth/login/', { username, password }),
  register: (username: string, email: string, password: string) =>
    apiClient.post('/auth/register/', { username, email, password }),
  logout: () => {
    localStorage.removeItem('token');
    return Promise.resolve();
  },
  
  // Wishlist
  getWishlist: () => apiClient.get('/wishlist/'),
  addToWishlist: (productId: number) =>
    apiClient.post('/wishlist/add/', { product_id: productId }),
  removeFromWishlist: (productId: number) =>
    apiClient.post('/wishlist/remove/', { product_id: productId }),
  
  // Sellers
  getSeller: (id: number) => apiClient.get(`/sellers/${id}/`),
  getSellerProducts: (id: number) =>
    apiClient.get(`/sellers/${id}/products/`),
};

export default apiClient;
