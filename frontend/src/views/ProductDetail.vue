<template>
  <div class="product-detail-container">
    <!-- Breadcrumb -->
    <el-breadcrumb class="breadcrumb" separator-icon="ArrowRight">
      <el-breadcrumb-item :to="{ name: 'home' }">{{ $t('nav.home') }}</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ name: 'products' }">{{ $t('nav.products') }}</el-breadcrumb-item>
      <el-breadcrumb-item v-if="product">{{ product.name }}</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- Loading State -->
    <el-skeleton v-if="loading" :rows="5" animated />

    <!-- Error State -->
    <el-alert v-if="error" type="error" :closable="false" class="error-alert">
      {{ error }}
    </el-alert>

    <!-- Product Details -->
    <div v-if="product && !loading" class="product-detail">
      <div class="product-content">
        <!-- Product Gallery -->
        <div class="product-gallery">
          <div class="main-image">
            <img :src="mainImage" :alt="product.name" />
          </div>
          <div class="thumbnail-gallery" v-if="product.images && product.images.length > 0">
            <div
              v-for="(image, index) in product.images"
              :key="index"
              class="thumbnail"
              :class="{ active: mainImage === image.image }"
              @click="mainImage = image.image"
            >
              <img :src="image.image" :alt="`${product.name} ${index}`" />
            </div>
          </div>
        </div>

        <!-- Product Info -->
        <div class="product-info">
          <!-- Category Badge -->
          <el-tag v-if="product.category_name" type="info" class="category-badge">
            {{ product.category_name }}
          </el-tag>

          <!-- Product Name -->
          <h1 class="product-name">{{ product.name }}</h1>

          <!-- Rating & Reviews -->
          <div class="rating-section">
            <el-rate v-model="averageRating" disabled show-score text-color="#ff9800" />
            <span class="review-count">({{ reviewCount }} {{ $t('product.reviews') }})</span>
          </div>

          <!-- Price Section -->
          <div class="price-section">
            <div class="price-container">
              <span class="current-price">{{ formatPrice(product.price) }}</span>
            <span v-if="product.compare_at_price && product.compare_at_price > product.price" class="compare-price">
              {{ formatPrice(product.compare_at_price) }}
              </span>
            </div>
            <div v-if="savingPercent" class="saving-badge">
              {{ $t('product.save') }} {{ savingPercent }}%
            </div>
          </div>

          <!-- Product Details Grid -->
          <div class="details-grid">
            <div class="detail-item">
              <span class="detail-label">{{ $t('product.sku') }}:</span>
              <span class="detail-value">{{ product.sku }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">{{ $t('product.type') }}:</span>
              <span class="detail-value">
                {{ product.product_type === 'physical' ? $t('product.physical') : $t('product.digital') }}
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-label">{{ $t('product.stock') }}:</span>
              <span class="detail-value" :class="{ 'out-of-stock': product.stock_quantity <= 0 }">
                {{ product.stock_quantity > 0 ? `${product.stock_quantity} ${$t('product.available')}` : $t('product.outOfStock') }}
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-label">{{ $t('product.category') }}:</span>
              <span class="detail-value">{{ product.category_name }}</span>
            </div>
          </div>

          <!-- Quantity Selector & Add to Cart -->
          <div class="action-section">
            <div class="quantity-selector">
              <span class="label">{{ $t('product.quantity') }}:</span>
              <el-input-number
                v-model="quantity"
                :min="1"
                :max="Math.min(10, product.stock_quantity)"
                :disabled="product.stock_quantity <= 0"
              />
            </div>
            <div class="action-buttons">
              <el-button
                type="primary"
                size="large"
                :disabled="product.stock_quantity <= 0"
                @click="addToCart"
                class="add-to-cart-btn"
              >
                <el-icon><ShoppingCart /></el-icon>
                {{ $t('product.addToCart') }}
              </el-button>
              <el-button
                size="large"
                :type="isInWishlist ? 'danger' : 'default'"
                @click="toggleWishlist"
                class="wishlist-btn"
              >
                <el-icon><Heart /></el-icon>
              </el-button>
            </div>
          </div>

          <!-- Seller Info -->
          <div v-if="product.seller" class="seller-info">
            <el-card class="seller-card">
              <template #header>
                <div class="card-header">
                  <span>{{ $t('product.seller') }}</span>
                </div>
              </template>
              <div class="seller-content">
                <p class="seller-name">{{ product.seller.store_name }}</p>
                <el-rate v-model="product.seller.rating" disabled show-score />
                <p class="seller-desc">{{ product.seller.description }}</p>
                <el-button type="primary" link>{{ $t('product.visitStore') }}</el-button>
              </div>
            </el-card>
          </div>

          <!-- Product Features -->
          <div v-if="product.features && product.features.length > 0" class="features-section">
            <h3>{{ $t('product.features') }}</h3>
            <ul class="features-list">
              <li v-for="(feature, index) in product.features" :key="index">
                <el-icon color="#409eff"><Check /></el-icon>
                {{ feature }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Product Description Tab -->
      <div class="product-tabs">
        <el-tabs>
          <el-tab-pane :label="$t('product.description')">
            <div class="description-content">{{ product.description }}</div>
          </el-tab-pane>
          <el-tab-pane :label="$t('product.reviews')">
            <div class="reviews-placeholder">
              {{ $t('product.noReviews') }}
            </div>
          </el-tab-pane>
          <el-tab-pane :label="$t('product.specifications')">
            <div class="specs-placeholder">
              {{ $t('product.specsComingSoon') }}
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- Related Products -->
      <div v-if="relatedProducts.length > 0" class="related-products">
        <h2>{{ $t('product.relatedProducts') }}</h2>
        <div class="products-grid">
          <div v-for="relProduct in relatedProducts" :key="relProduct.id" class="product-card">
            <div class="product-image">
              <img :src="relProduct.images[0]?.image || defaultImage" :alt="relProduct.name" />
              <div class="overlay">
                <router-link :to="{ name: 'product-detail', params: { slug: relProduct.slug } }" class="view-btn">
                  {{ $t('product.viewDetails') }}
                </router-link>
              </div>
            </div>
            <div class="product-details">
              <h4 class="name">{{ relProduct.name }}</h4>
              <div class="price">{{ formatPrice(relProduct.price) }}</div>
              <el-button type="primary" size="small" @click="addRelatedToCart(relProduct)">
                {{ $t('product.addToCart') }}
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ShoppingCart, Heart, Check } from '@element-plus/icons-vue'
import productService from '@/services/productService'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const product = ref(null)
const loading = ref(true)
const error = ref(null)
const mainImage = ref('')
const quantity = ref(1)
const isInWishlist = ref(false)
const relatedProducts = ref([])
const averageRating = ref(4.5)
const reviewCount = ref(0)
const defaultImage = ref('https://via.placeholder.com/400x400?text=No+Image')

const savingPercent = computed(() => {
  if (!product.value || !product.value.compare_at_price) return 0
  const saving = ((product.value.compare_at_price - product.value.price) / product.value.compare_at_price) * 100
  return Math.round(saving)
})

const fetchProduct = async () => {
  try {
    loading.value = true
    error.value = null
    const slug = route.params.slug
    const response = await productService.getProduct(slug)
    product.value = response.data
    
    // Set main image
    if (product.value.images && product.value.images.length > 0) {
      mainImage.value = product.value.images[0].image
    }
    
    // Fetch related products (same category)
    await fetchRelatedProducts()
    
    // Check if in wishlist
    if (authStore.isAuthenticated) {
      await checkWishlistStatus()
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load product'
    console.error('Error fetching product:', err)
  } finally {
    loading.value = false
  }
}

const fetchRelatedProducts = async () => {
  try {
    const response = await productService.getProducts({
      category: product.value.category,
      page_size: 8
    })
    // Filter out the current product and limit to 4 related products
    relatedProducts.value = response.data.results
      .filter(p => p.id !== product.value.id)
      .slice(0, 4)
  } catch (err) {
    console.error('Error fetching related products:', err)
  }
}

const checkWishlistStatus = async () => {
  try {
    const response = await productService.getWishlist()
    isInWishlist.value = response.data.results.some(item => item.product.id === product.value.id)
  } catch (err) {
    console.error('Error checking wishlist:', err)
  }
}

const addToCart = async () => {
  if (!product.value) return
  
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    ElMessage.warning('Please login to add items to cart')
    router.push({ name: 'login' })
    return
  }
  
  const result = await cartStore.addItem(product.value.id, quantity.value)
  if (result.success) {
    quantity.value = 1
  }
}

const addRelatedToCart = async (relProduct) => {
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    ElMessage.warning('Please login to add items to cart')
    router.push({ name: 'login' })
    return
  }
  
  await cartStore.addItem(relProduct.id, 1)
}

const toggleWishlist = async () => {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login' })
    return
  }
  
  try {
    if (isInWishlist.value) {
      // Remove from wishlist
      const response = await productService.getWishlist()
      const wishlistItem = response.data.results.find(item => item.product.id === product.value.id)
      if (wishlistItem) {
        await productService.removeFromWishlist(wishlistItem.id)
        isInWishlist.value = false
        ElMessage.success('Removed from wishlist')
      }
    } else {
      // Add to wishlist
      await productService.addToWishlist(product.value.id)
      isInWishlist.value = true
      ElMessage.success('Added to wishlist')
    }
  } catch (err) {
    ElMessage.error('Failed to update wishlist')
    console.error('Error updating wishlist:', err)
  }
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(price)
}

onMounted(() => {
  fetchProduct()
})
</script>

<style scoped>
.product-detail-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.breadcrumb {
  margin-bottom: 30px;
}

.error-alert {
  margin-bottom: 20px;
}

.product-detail {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.product-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

/* Gallery Section */
.product-gallery {
  display: flex;
  flex-direction: column;
  gap: 15px;
  position: sticky;
  top: 20px;
}

.main-image {
  width: 100%;
  aspect-ratio: 1;
  background-color: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.main-image:hover img {
  transform: scale(1.05);
}

.thumbnail-gallery {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.thumbnail {
  aspect-ratio: 1;
  border: 2px solid transparent;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #f5f5f5;
}

.thumbnail:hover {
  border-color: #e0e0e0;
}

.thumbnail.active {
  border-color: #409eff;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Info Section */
.product-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.category-badge {
  width: fit-content;
}

.product-name {
  font-size: 28px;
  font-weight: 600;
  margin: 10px 0;
  line-height: 1.3;
}

.rating-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.review-count {
  color: #909399;
  font-size: 14px;
}

/* Price Section */
.price-section {
  padding: 15px 0;
  border-top: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
}

.price-container {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 10px;
}

.current-price {
  font-size: 32px;
  font-weight: 700;
  color: #f56c6c;
}

.compare-price {
  font-size: 16px;
  color: #909399;
  text-decoration: line-through;
}

.saving-badge {
  display: inline-block;
  background-color: #f56c6c;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

/* Details Grid */
.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  padding: 15px 0;
  border-bottom: 1px solid #ebeef5;
}

.detail-item {
  display: flex;
  justify-content: space-between;
}

.detail-label {
  color: #606266;
  font-weight: 500;
}

.detail-value {
  color: #303133;
  font-weight: 500;
}

.detail-value.out-of-stock {
  color: #f56c6c;
}

/* Action Section */
.action-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin: 20px 0;
}

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quantity-selector .label {
  font-weight: 500;
  color: #606266;
}

:deep(.el-input-number) {
  width: 100px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.add-to-cart-btn {
  flex: 1;
  height: 50px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 4px;
}

.wishlist-btn {
  width: 50px;
  height: 50px;
  padding: 0;
  border-radius: 4px;
}

/* Seller Info */
.seller-info {
  margin-top: 20px;
}

.seller-card {
  border-radius: 8px;
}

:deep(.seller-card .el-card__header) {
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
}

.seller-content {
  padding: 15px;
}

.seller-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 10px 0;
}

.seller-desc {
  color: #606266;
  font-size: 14px;
  margin: 10px 0;
  line-height: 1.5;
}

/* Features Section */
.features-section {
  margin-top: 20px;
}

.features-section h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 600;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.features-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  color: #606266;
  font-size: 14px;
}

.features-list :deep(.el-icon) {
  flex-shrink: 0;
}

/* Tabs Section */
.product-tabs {
  margin-top: 40px;
  border-top: 1px solid #ebeef5;
  padding-top: 20px;
}

.description-content {
  padding: 20px;
  line-height: 1.8;
  color: #606266;
  white-space: pre-wrap;
}

.reviews-placeholder,
.specs-placeholder {
  padding: 40px;
  text-align: center;
  color: #909399;
  font-size: 14px;
}

/* Related Products */
.related-products {
  margin-top: 60px;
  padding-top: 40px;
  border-top: 1px solid #ebeef5;
}

.related-products h2 {
  margin: 0 0 25px 0;
  font-size: 22px;
  font-weight: 600;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.product-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.product-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.product-image {
  position: relative;
  aspect-ratio: 1;
  background-color: #f5f5f5;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.1);
}

.overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .overlay {
  opacity: 1;
}

.view-btn {
  background-color: white;
  color: #409eff;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.view-btn:hover {
  background-color: #409eff;
  color: white;
}

.product-details {
  padding: 15px;
}

.product-details .name {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-details .price {
  font-size: 16px;
  font-weight: 700;
  color: #f56c6c;
  margin: 8px 0 12px 0;
}

/* Responsive */
@media (max-width: 768px) {
  .product-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .product-gallery {
    position: relative;
    top: 0;
  }

  .details-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .wishlist-btn {
    width: 100%;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }

  .product-name {
    font-size: 22px;
  }

  .current-price {
    font-size: 24px;
  }
}
</style>
