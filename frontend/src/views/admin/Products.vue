<template>
  <div class="admin-products">
    <div class="page-header">
      <h1>{{ $t('admin.products') }}</h1>
      <el-button type="primary" @click="$router.push('/admin/products/create')">
        <el-icon><Plus /></el-icon>
        {{ $t('admin.createProduct') }}
      </el-button>
    </div>
    
    <el-card>
      <el-table :data="products" v-loading="loading" stripe @current-change="handlePageChange">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" :label="$t('product.name')" min-width="200" />
        <el-table-column prop="category_name" :label="$t('product.category')" width="150" />
        <el-table-column prop="price" :label="$t('product.price')" width="120">
          <template #default="{ row }">
            {{ formatCurrency(row.price) }}
          </template>
        </el-table-column>
        <el-table-column prop="stock_quantity" :label="$t('product.stock')" width="100" />
        <el-table-column prop="is_active" label="Active" width="100" align="center">
          <template #default="{ row }">
            <el-switch v-model="row.is_active" @change="toggleActive(row)" />
          </template>
        </el-table-column>
        <el-table-column :label="$t('common.actions')" width="180" fixed="right">
          <template #default="{ row }">
            <el-button 
              size="small" 
              @click="editProduct(row.id)"
              type="primary" 
              text
            >
              {{ $t('common.edit') }}
            </el-button>
            <el-popconfirm
              title="Delete this product?"
              confirm-button-text="Yes"
              cancel-button-text="No"
              @confirm="deleteProduct(row.id)"
            >
              <template #reference>
                <el-button size="small" type="danger" text>
                  {{ $t('common.delete') }}
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 20px; text-align: right"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import api from '@/services/api'

const router = useRouter()
const loading = ref(false)
const products = ref([])

const pagination = ref({
  page: 1,
  page_size: 20,
  total: 0
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(amount || 0)
}

const fetchProducts = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/products/products/', {
      params: {
        page: pagination.value.page,
        page_size: pagination.value.page_size
      }
    })
    
    const data = response.data
    if (data.results) {
      products.value = data.results
      pagination.value.total = data.count
    } else if (Array.isArray(data)) {
      products.value = data
      pagination.value.total = data.length
    }
  } catch (error) {
    ElMessage.error('Failed to load products')
    console.error('Products fetch error:', error)
  } finally {
    loading.value = false
  }
}

const editProduct = (id) => {
  router.push(`/admin/products/${id}/edit`)
}

const deleteProduct = async (id) => {
  try {
    await api.delete(`/api/products/products/${id}/`)
    ElMessage.success('Product deleted successfully')
    await fetchProducts()
  } catch (error) {
    ElMessage.error('Failed to delete product')
    console.error('Delete error:', error)
  }
}

const toggleActive = async (row) => {
  try {
    await api.patch(`/api/products/products/${row.id}/`, {
      is_active: row.is_active
    })
    ElMessage.success('Product updated')
  } catch (error) {
    ElMessage.error('Failed to update product')
    console.error('Toggle error:', error)
  }
}

const handlePageChange = () => {
  fetchProducts()
}

onMounted(async () => {
  await fetchProducts()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
