<template>
  <el-card class="product-card">
    <template #header>
      <img :src="productImage" :alt="product.name" class="product-image" />
      <el-tag v-if="product.product_type === 'digital'" type="info" size="small" class="product-type-tag">
        {{ $t('product.digital') }}
      </el-tag>
      <el-tag v-if="product.discount_percentage > 0" type="danger" size="small" class="discount-tag">
        -{{ product.discount_percentage }}%
      </el-tag>
    </template>
    
    <div class="product-info" @click="goToProduct">
      <h4 class="product-name">{{ product.name }}</h4>
      <div class="product-rating">
        <el-rate v-model="product.average_rating" disabled show-score :max="5" />
      </div>
      <div class="product-price">
        <span class="current-price">{{ formatPrice(product.price) }}</span>
        <span v-if="product.compare_at_price" class="old-price">
          {{ formatPrice(product.compare_at_price) }}
        </span>
      </div>
      <div class="product-seller">
        <el-icon><User /></el-icon>
        <span>{{ product.seller_name }}</span>
      </div>
    </div>
    
    <template #footer>
      <div class="product-actions">
        <el-button type="primary" @click="addToCart" :loading="adding">
          {{ $t('product.addToCart') }}
        </el-button>
        <el-button circle @click="toggleWishlist">
          <el-icon><Star v-if="!inWishlist" /><StarFilled v-else /></el-icon>
        </el-button>
      </div>
    </template>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { ElMessage } from 'element-plus'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const cartStore = useCartStore()
const adding = ref(false)
const inWishlist = ref(false)

const productImage = computed(() => {
  if (props.product.images && props.product.images.length > 0) {
    return props.product.images[0].image
  }
  return 'https://via.placeholder.com/300x300?text=No+Image'
})

function formatPrice(price) {
  return `${parseFloat(price).toFixed(2)} ₽`
}

function goToProduct() {
  router.push({ name: 'product-detail', params: { slug: props.product.slug } })
}

async function addToCart() {
  adding.value = true
  const result = await cartStore.addItem(props.product.id, 1)
  adding.value = false
  
  if (result.success) {
    ElMessage.success('Added to cart')
  }
}

function toggleWishlist() {
  inWishlist.value = !inWishlist.value
  ElMessage.success(inWishlist.value ? 'Added to wishlist' : 'Removed from wishlist')
}
</script>

<style scoped>
.product-card {
  height: 100%;
  cursor: pointer;
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.product-type-tag {
  position: absolute;
  top: 10px;
  left: 10px;
}

.discount-tag {
  position: absolute;
  top: 10px;
  right: 10px;
}

.product-info {
  padding: 12px 0;
}

.product-name {
  font-size: 16px;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.product-rating {
  margin-bottom: 8px;
}

.product-price {
  margin-bottom: 8px;
}

.current-price {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  margin-right: 8px;
}

.old-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
}

.product-seller {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #666;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.product-actions .el-button {
  flex: 1;
}
</style>
