<template>
  <div class="home">
    <el-carousel :interval="5000" height="400px" class="hero-carousel">
      <el-carousel-item v-for="item in banners" :key="item">
        <div class="carousel-item" :style="{ backgroundColor: item.color }">
          <h2>{{ item.title }}</h2>
          <p>{{ item.description }}</p>
        </div>
      </el-carousel-item>
    </el-carousel>
    
    <div class="container">
      <section class="section">
        <h2>{{ $t('nav.categories') }}</h2>
        <el-row :gutter="20">
          <el-col :xs="12" :sm="8" :md="6" v-for="category in categories" :key="category.id">
            <el-card shadow="hover" class="category-card" @click="goToCategory(category.slug)">
              <div class="category-content">
                <el-icon :size="40"><Box /></el-icon>
                <p>{{ category.name }}</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </section>
      
      <section class="section">
        <h2>Popular Products</h2>
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="product in products" :key="product.id">
            <ProductCard :product="product" />
          </el-col>
        </el-row>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductStore } from '@/stores/product'
import ProductCard from '@/components/product/ProductCard.vue'

const router = useRouter()
const productStore = useProductStore()

const banners = ref([
  { title: 'Welcome to Marketplace', description: 'Shop the best products', color: '#409eff' },
  { title: 'Seller Registration', description: 'Start selling today', color: '#67c23a' },
  { title: 'Digital Products', description: 'Instant delivery', color: '#e6a23c' }
])

const categories = ref([])
const products = ref([])

onMounted(async () => {
  await productStore.fetchCategories()
  categories.value = productStore.categories.slice(0, 8)
  
  await productStore.fetchProducts({ ordering: '-sold_count', page_size: 8 })
  products.value = productStore.products
})

function goToCategory(slug) {
  router.push({ name: 'products', query: { category: slug } })
}
</script>

<style scoped>
.home {
  padding: 0;
}

.hero-carousel {
  margin-bottom: 40px;
}

.carousel-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: white;
}

.carousel-item h2 {
  font-size: 48px;
  margin-bottom: 20px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.section {
  margin-bottom: 60px;
}

.section h2 {
  margin-bottom: 24px;
  font-size: 28px;
}

.category-card {
  cursor: pointer;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.category-card:hover {
  transform: translateY(-5px);
}

.category-content {
  text-align: center;
  padding: 20px;
}

.category-content p {
  margin-top: 12px;
  font-weight: 500;
}
</style>
