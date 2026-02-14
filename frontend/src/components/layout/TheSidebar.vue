<template>
  <div class="sidebar">
    <h3>{{ $t('nav.categories') }}</h3>
    <el-menu :default-active="activeCategory" @select="selectCategory">
      <el-menu-item v-for="category in categories" :key="category.id" :index="category.slug">
        {{ category.name }}
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductStore } from '@/stores/product'

const router = useRouter()
const productStore = useProductStore()
const categories = ref([])
const activeCategory = ref('')

onMounted(async () => {
  const result = await productStore.fetchCategories()
  if (result.success) {
    categories.value = productStore.categories
  }
})

function selectCategory(categorySlug) {
  router.push({ name: 'products', query: { category: categorySlug } })
}
</script>

<style scoped>
.sidebar {
  padding: 20px;
}

h3 {
  margin-bottom: 16px;
  font-size: 16px;
}

.el-menu {
  border: none;
}
</style>
