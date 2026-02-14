<template>
  <div class="admin-product-form">
    <div class="page-header">
      <el-button @click="goBack" type="info">
        <el-icon><ArrowLeft /></el-icon>
        {{ $t('common.back') }}
      </el-button>
      <h1>{{ isEdit ? $t('admin.editProduct') : $t('admin.createProduct') }}</h1>
    </div>

    <el-card>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="140px"
        @submit.prevent="submitForm"
      >
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="Name" prop="name">
              <el-input v-model="form.name" placeholder="Product name" />
            </el-form-item>

            <el-form-item label="SKU" prop="sku">
              <el-input v-model="form.sku" placeholder="Auto-generated SKU">
                <template #append>
                  <el-button @click="generateSKU">{{ $t('common.generate') }}</el-button>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item label="Category" prop="category">
              <el-select v-model="form.category" placeholder="Select category" :loading="categoriesLoading">
                <el-option
                  v-for="cat in categories"
                  :key="cat.id"
                  :label="cat.name"
                  :value="cat.id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="Product Type" prop="product_type">
              <el-select v-model="form.product_type" placeholder="Select type">
                <el-option label="Physical Product" value="physical" />
                <el-option label="Digital Product" value="digital" />
              </el-select>
            </el-form-item>

            <el-form-item label="Price" prop="price">
              <el-input-number v-model="form.price" :min="0.01" :step="0.01" placeholder="0.00" />
            </el-form-item>

            <el-form-item label="Compare Price" prop="compare_at_price">
              <el-input-number
                v-model="form.compare_at_price"
                :min="0"
                :step="0.01"
                placeholder="Optional - for discounts"
              />
            </el-form-item>

            <el-form-item label="Stock" prop="stock_quantity">
              <el-input-number v-model="form.stock_quantity" :min="0" placeholder="0" />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12">
            <el-form-item label="Description" prop="description">
              <el-input
                v-model="form.description"
                type="textarea"
                rows="8"
                placeholder="Product description"
              />
            </el-form-item>

            <el-form-item prop="is_active">
              <template #label>
                <span>{{ $t('admin.active') }}</span>
              </template>
              <el-switch v-model="form.is_active" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">
            {{ isEdit ? $t('common.update') : $t('common.create') }}
          </el-button>
          <el-button @click="goBack">{{ $t('common.cancel') }}</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()

const formRef = ref(null)
const loading = ref(false)
const categoriesLoading = ref(false)
const isEdit = ref(false)
const categories = ref([])

const form = ref({
  name: '',
  sku: '',
  category: null,
  product_type: 'physical',
  price: 0,
  compare_at_price: null,
  stock_quantity: 0,
  description: '',
  is_active: true
})

const rules = {
  name: [{ required: true, message: 'Product name is required', trigger: 'blur' }],
  sku: [{ required: true, message: 'SKU is required', trigger: 'blur' }],
  category: [{ required: true, message: 'Category is required', trigger: 'change' }],
  price: [{ required: true, message: 'Price is required', trigger: 'blur' }],
  description: [{ required: true, message: 'Description is required', trigger: 'blur' }]
}

const generateSKU = () => {
  const timestamp = Date.now().toString(36).toUpperCase()
  const random = Math.random().toString(36).substring(2, 8).toUpperCase()
  form.value.sku = `SKU-${timestamp}-${random}`
}

const fetchCategories = async () => {
  categoriesLoading.value = true
  try {
    const response = await api.get('/api/products/categories/')
    categories.value = response.data.results || response.data
  } catch (error) {
    ElMessage.error('Failed to load categories')
    console.error('Categories fetch error:', error)
  } finally {
    categoriesLoading.value = false
  }
}

const fetchProduct = async (id) => {
  try {
    const response = await api.get(`/api/products/products/${id}/`)
    const product = response.data
    form.value = {
      name: product.name,
      sku: product.sku,
      category: product.category,
      product_type: product.product_type,
      price: product.price,
      compare_at_price: product.compare_at_price,
      stock_quantity: product.stock_quantity,
      description: product.description,
      is_active: product.is_active
    }
  } catch (error) {
    ElMessage.error('Failed to load product')
    console.error('Product fetch error:', error)
  }
}

const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate()

  loading.value = true
  try {
    if (isEdit.value) {
      // Update existing product
      await api.patch(`/api/products/products/${route.params.id}/`, form.value)
      ElMessage.success('Product updated successfully')
    } else {
      // Create new product
      await api.post('/api/products/products/', form.value)
      ElMessage.success('Product created successfully')
    }
    await router.push('/admin/products')
  } catch (error) {
    const errorMsg = error.response?.data?.detail || error.response?.data?.message || 'Error saving product'
    ElMessage.error(errorMsg)
    console.error('Submit error:', error.response?.data || error)
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/admin/products')
}

onMounted(async () => {
  // Load categories
  await fetchCategories()

  // Check if this is edit mode
  if (route.params.id) {
    isEdit.value = true
    await fetchProduct(route.params.id)
  } else {
    // Generate SKU for new product
    generateSKU()
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  flex: 1;
}
</style>
