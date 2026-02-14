<template>
  <div class="product-list-page">
    <el-row :gutter="20">
      <!-- Sidebar Filters -->
      <el-col :xs="0" :md="6">
        <el-card class="filter-card">
          <template #header>
            <div class="filter-header">
              <span>{{ $t('products.filter') }}</span>
              <el-button link @click="resetFilters">{{ $t('products.resetFilter') }}</el-button>
            </div>
          </template>
          
          <!-- Categories -->
          <div class="filter-section">
            <h4>{{ $t('nav.categories') }}</h4>
            <el-checkbox-group v-model="filters.categories">
              <el-checkbox v-for="category in categories" :key="category.id" :label="category.id">
                {{ category.name }}
              </el-checkbox>
            </el-checkbox-group>
          </div>
          
          <el-divider />
          
          <!-- Price Range -->
          <div class="filter-section">
            <h4>{{ $t('products.priceRange') }}</h4>
            <el-slider v-model="filters.priceRange" :min="0" :max="100000" :step="1000" range />
            <div class="price-inputs">
              <el-input v-model.number="filters.priceRange[0]" size="small" :placeholder="$t('products.minPrice')" />
              <span>-</span>
              <el-input v-model.number="filters.priceRange[1]" size="small" :placeholder="$t('products.maxPrice')" />
            </div>
          </div>
          
          <el-divider />
          
          <!-- Product Type -->
          <div class="filter-section">
            <h4>{{ $t('product.name') }}</h4>
            <el-radio-group v-model="filters.productType">
              <el-radio label="">{{ $t('products.allProducts') }}</el-radio>
              <el-radio label="physical">{{ $t('product.physical') }}</el-radio>
              <el-radio label="digital">{{ $t('product.digital') }}</el-radio>
            </el-radio-group>
          </div>
          
          <el-button type="primary" style="width: 100%; margin-top: 20px" @click="applyFilters">
            {{ $t('products.applyFilter') }}
          </el-button>
        </el-card>
      </el-col>
      
      <!-- Products Grid -->
      <el-col :xs="24" :md="18">
        <!-- Header -->
        <div class="products-header">
          <div>
            <h1>{{ $t('products.title') }}</h1>
            <p class="results-count" v-if="pagination.total">
              {{ $t('products.showingResults') }} {{ products.length }} {{ $t('products.of') }} {{ pagination.total }}
            </p>
          </div>
          
          <div class="header-actions">
            <el-select v-model="sortBy" @change="fetchProducts" style="width: 200px">
              <el-option :label="$t('products.popularFirst')" value="-sold_count" />
              <el-option :label="$t('products.newestFirst')" value="-created_at" />
              <el-option :label="$t('products.priceAsc')" value="price" />
              <el-option :label="$t('products.priceDesc')" value="-price" />
            </el-select>
          </div>
        </div>
        
        <!-- Products Grid -->
        <div v-loading="loading" class="products-grid">
          <el-empty v-if="!loading && !products.length" :description="$t('products.noProducts')" />
          
          <el-card v-for="product in products" :key="product.id" shadow="hover" class="product-card" @click="goToProduct(product)">
            <div class="product-image">
              <el-image :src="product.image || '/placeholder.jpg'" fit="cover" />
              <el-tag v-if="product.product_type === 'digital'" class="product-type-tag" type="info">
                {{ $t('product.digital') }}
              </el-tag>
            </div>
            
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-category">{{ product.category_name }}</p>
              
              <div class="product-rating">
                <el-rate v-model="product.rating" disabled show-score text-color="#ff9900" score-template="{value}" />
                <span class="reviews-count">({{ product.reviews_count || 0 }})</span>
              </div>
              
              <div class="product-footer">
                <div class="price-section">
                  <span class="price">{{ formatCurrency(product.price) }}</span>
                  <span v-if="product.old_price" class="old-price">{{ formatCurrency(product.old_price) }}</span>
                </div>
                
                <el-button type="primary" size="small" @click.stop="addToCart(product)">
                  <el-icon><ShoppingCart /></el-icon>
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
        
        <!-- Pagination -->
        <el-pagination
          v-if="pagination.total > pagination.pageSize"
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[20, 40, 60, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchProducts"
          @current-change="fetchProducts"
          class="pagination"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ShoppingCart } from '@element-plus/icons-vue'
import { useCartStore } from '@/stores/cart'
import api from '@/services/api'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(false)
const products = ref([])
const categories = ref([])
const sortBy = ref('-sold_count')

const filters = reactive({
  categories: [],
  priceRange: [0, 100000],
  productType: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 20,
  total: 0
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(amount || 0)
}

const fetchCategories = async () => {
  try {
    const response = await api.get('/products/categories/')
    categories.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  }
}

const fetchProducts = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      ordering: sortBy.value
    }
    
    if (filters.categories.length) {
      params.category = filters.categories.join(',')
    }
    
    if (filters.priceRange[0] > 0) {
      params.min_price = filters.priceRange[0]
    }
    
    if (filters.priceRange[1] < 100000) {
      params.max_price = filters.priceRange[1]
    }
    
    if (filters.productType) {
      params.is_digital = filters.productType === 'digital'
    }
    
    const response = await api.get('/products/products/', { params })
    products.value = response.data.results || []
    pagination.total = response.data.count || 0
  } catch (error) {
    console.error('Failed to fetch products:', error)
    ElMessage.error('Failed to load products')
  } finally {
    loading.value = false
  }
}

const applyFilters = () => {
  pagination.currentPage = 1
  fetchProducts()
}

const resetFilters = () => {
  filters.categories = []
  filters.priceRange = [0, 100000]
  filters.productType = ''
  pagination.currentPage = 1
  fetchProducts()
}

const addToCart = async (product) => {
  try {
    await cartStore.addItem(product.id, 1)
    ElMessage.success('Added to cart')
  } catch (error) {
    ElMessage.error('Failed to add to cart')
  }
}

const goToProduct = (product) => {
  router.push({ name: 'product-detail', params: { slug: product.slug } })
}

onMounted(() => {
  fetchCategories()
  fetchProducts()
})
</script>

<style scoped>
.product-list-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.filter-card {
  position: sticky;
  top: 80px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-section {
  margin: 20px 0;
}

.filter-section h4 {
  margin-bottom: 15px;
  color: #303133;
  font-size: 14px;
  font-weight: 600;
}

.filter-section .el-checkbox {
  display: block;
  margin: 10px 0;
}

.filter-section .el-radio {
  display: block;
  margin: 10px 0;
}

.price-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}

.products-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 25px;
}

.products-header h1 {
  margin: 0 0 10px;
  color: #303133;
}

.results-count {
  color: #909399;
  font-size: 14px;
  margin: 0;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  min-height: 400px;
}

.product-card {
  cursor: pointer;
  transition: transform 0.2s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  position: relative;
  width: 100%;
  height: 250px;
  overflow: hidden;
  border-radius: 4px;
  margin-bottom: 15px;
}

.product-image .el-image {
  width: 100%;
  height: 100%;
}

.product-type-tag {
  position: absolute;
  top: 10px;
  right: 10px;
}

.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-size: 16px;
  margin: 0 0 8px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.product-category {
  font-size: 12px;
  color: #909399;
  margin: 0 0 10px;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 15px;
}

.reviews-count {
  font-size: 12px;
  color: #909399;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.price-section {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.price {
  font-size: 20px;
  font-weight: 600;
  color: #409eff;
}

.old-price {
  font-size: 14px;
  color: #909399;
  text-decoration: line-through;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .products-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }
  
  .product-image {
    height: 180px;
  }
}
</style>
