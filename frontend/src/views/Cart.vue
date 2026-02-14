<template>
  <div class="cart-page">
    <div class="container">
      <h1>{{ $t('cart.title') }}</h1>
      
      <el-empty v-if="!cartItems.length && !loading" :description="$t('cart.empty')">
        <el-button type="primary" @click="$router.push('/products')">
          {{ $t('nav.products') }}
        </el-button>
      </el-empty>
      
      <el-row :gutter="20" v-else>
        <!-- Cart Items -->
        <el-col :xs="24" :md="16">
          <div v-loading="loading">
            <el-card v-for="item in cartItems" :key="item.id" class="cart-item" shadow="hover">
              <el-row :gutter="20">
                <el-col :xs="8" :sm="6">
                  <el-image :src="item.product.image || '/placeholder.jpg'" fit="cover" class="item-image" />
                </el-col>
                
                <el-col :xs="16" :sm="18">
                  <div class="item-details">
                    <div class="item-header">
                      <h3 class="item-name" @click="goToProduct(item.product.id)">{{ item.product.name }}</h3>
                      <el-button link type="danger" @click="removeItem(item.id)">
                        <el-icon><Delete /></el-icon>
                      </el-button>
                    </div>
                    
                    <p class="item-category">{{ item.product.category_name }}</p>
                    
                    <el-tag v-if="item.product.is_digital" type="info" size="small">
                      {{ $t('product.digital') }}
                    </el-tag>
                    
                    <div class="item-footer">
                      <div class="quantity-control">
                        <el-input-number 
                          v-model="item.quantity" 
                          :min="1" 
                          :max="item.product.is_digital ? 1 : item.product.stock"
                          :disabled="item.product.is_digital"
                          @change="updateQuantity(item.id, item.quantity)"
                          size="small"
                        />
                      </div>
                      
                      <div class="price-info">
                        <span class="price">{{ formatCurrency(item.product.price * item.quantity) }}</span>
                        <span class="unit-price" v-if="item.quantity > 1">
                          {{ formatCurrency(item.product.price) }} × {{ item.quantity }}
                        </span>
                      </div>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </el-card>
          </div>
        </el-col>
        
        <!-- Order Summary -->
        <el-col :xs="24" :md="8">
          <el-card class="summary-card" shadow="always">
            <template #header>
              <h3>{{ $t('cart.subtotal') }}</h3>
            </template>
            
            <el-statistic :value="cartTotal" :precision="2" prefix="₽">
              <template #title>
                <span>{{ $t('cart.total') }}</span>
              </template>
            </el-statistic>
            
            <el-divider />
            
            <div class="summary-details">
              <div class="summary-row">
                <span>{{ $t('cart.quantity') }}:</span>
                <strong>{{ totalItems }}</strong>
              </div>
            </div>
            
            <el-button 
              type="primary" 
              size="large" 
              style="width: 100%; margin-top: 20px"
              :disabled="!cartItems.length"
              @click="$router.push('/checkout')"
            >
              {{ $t('cart.checkout') }}
            </el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(false)

const cartItems = computed(() => cartStore.items)
const cartTotal = computed(() => cartStore.total)
const totalItems = computed(() => cartItems.value.reduce((sum, item) => sum + item.quantity, 0))

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(amount || 0)
}

const updateQuantity = async (itemId, quantity) => {
  try {
    await cartStore.updateItemQuantity(itemId, quantity)
  } catch (error) {
    ElMessage.error('Failed to update quantity')
  }
}

const removeItem = async (itemId) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to remove this item?',
      'Confirm',
      {
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
        type: 'warning'
      }
    )
    
    await cartStore.removeItem(itemId)
    ElMessage.success('Item removed from cart')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to remove item')
    }
  }
}

const goToProduct = (productId) => {
  router.push(`/products/${productId}`)
}

onMounted(async () => {
  loading.value = true
  await cartStore.fetchCart()
  loading.value = false
})
</script>

<style scoped>
.cart-page {
  min-height: calc(100vh - 200px);
  padding: 20px;
  background-color: #f5f7fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 30px;
  color: #303133;
}

.cart-item {
  margin-bottom: 20px;
}

.item-image {
  width: 100%;
  height: 120px;
  border-radius: 4px;
}

.item-details {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.item-name {
  margin: 0;
  font-size: 16px;
  color: #303133;
  cursor: pointer;
  flex: 1;
}

.item-name:hover {
  color: #409eff;
}

.item-category {
  margin: 8px 0;
  color: #909399;
  font-size: 14px;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 15px;
}

.price-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.price {
  font-size: 20px;
  font-weight: 600;
  color: #409eff;
}

.unit-price {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.summary-card {
  position: sticky;
  top: 80px;
}

.summary-details {
  margin: 20px 0;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
  font-size: 14px;
}

@media (max-width: 768px) {
  .item-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .price-info {
    width: 100%;
    align-items: flex-start;
  }
}
</style>
