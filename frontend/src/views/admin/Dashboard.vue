<template>
  <div class="admin-dashboard">
    <h1>{{ $t('admin.dashboard') }}</h1>
    
    <!-- Statistics Cards -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card stat-users">
          <el-statistic :value="stats.totalUsers">
            <template #title>
              <div class="stat-title">
                <el-icon><User /></el-icon>
                <span>{{ $t('admin.totalUsers') }}</span>
              </div>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card stat-products">
          <el-statistic :value="stats.totalProducts">
            <template #title>
              <div class="stat-title">
                <el-icon><Box /></el-icon>
                <span>{{ $t('admin.totalProducts') }}</span>
              </div>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card stat-orders">
          <el-statistic :value="stats.totalOrders">
            <template #title>
              <div class="stat-title">
                <el-icon><Document /></el-icon>
                <span>{{ $t('admin.totalOrders') }}</span>
              </div>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card stat-revenue">
          <el-statistic :value="stats.totalRevenue" :precision="2" prefix="₽">
            <template #title>
              <div class="stat-title">
                <el-icon><Money /></el-icon>
                <span>{{ $t('admin.totalRevenue') }}</span>
              </div>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- Charts Row -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <span>{{ $t('admin.recentOrders') }}</span>
          </template>
          <el-table :data="recentOrders" stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="user_email" :label="$t('auth.email')" />
            <el-table-column prop="total_price" :label="$t('order.total')" width="120">
              <template #default="{ row }">
                {{ formatCurrency(row.total_price) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" :label="$t('order.status')" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <span>{{ $t('admin.recentUsers') }}</span>
          </template>
          <el-table :data="recentUsers" stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="email" :label="$t('auth.email')" />
            <el-table-column prop="user_type" :label="$t('profile.accountType')" width="100">
              <template #default="{ row }">
                <el-tag :type="getUserTypeTag(row.user_type)" size="small">
                  {{ row.user_type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="is_verified" :label="$t('profile.verificationStatus')" width="100">
              <template #default="{ row }">
                <el-icon v-if="row.is_verified" color="#67c23a"><SuccessFilled /></el-icon>
                <el-icon v-else color="#f56c6c"><CircleClose /></el-icon>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- Quick Actions -->
    <el-card class="quick-actions">
      <template #header>
        <span>{{ $t('admin.quickActions') }}</span>
      </template>
      <el-space wrap>
        <el-button type="primary" @click="$router.push('/admin/products')">
          <el-icon><Box /></el-icon>
          {{ $t('admin.manageProducts') }}
        </el-button>
        <el-button type="success" @click="$router.push('/admin/users')">
          <el-icon><User /></el-icon>
          {{ $t('admin.manageUsers') }}
        </el-button>
        <el-button type="warning" @click="$router.push('/admin/orders')">
          <el-icon><Document /></el-icon>
          {{ $t('admin.manageOrders') }}
        </el-button>
        <el-button type="info" @click="$router.push('/admin/categories')">
          <el-icon><FolderOpened /></el-icon>
          {{ $t('admin.manageCategories') }}
        </el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, Box, Document, Money, FolderOpened, SuccessFilled, CircleClose } from '@element-plus/icons-vue'
import api from '@/services/api'

const stats = ref({
  totalUsers: 0,
  totalProducts: 0,
  totalOrders: 0,
  totalRevenue: 0
})

const recentOrders = ref([])
const recentUsers = ref([])

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(amount || 0)
}

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    processing: 'info',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getUserTypeTag = (type) => {
  const types = {
    buyer: 'success',
    seller: 'warning',
    admin: 'danger'
  }
  return types[type] || 'info'
}

const fetchDashboardData = async () => {
  try {
    // Mock data - replace with actual API calls
    stats.value = {
      totalUsers: 156,
      totalProducts: 423,
      totalOrders: 89,
      totalRevenue: 156789.50
    }
    
    recentOrders.value = [
      { id: 1, user_email: 'buyer@example.com', total_price: 1500, status: 'completed' },
      { id: 2, user_email: 'user@test.com', total_price: 2300, status: 'processing' },
      { id: 3, user_email: 'customer@mail.com', total_price: 890, status: 'pending' }
    ]
    
    recentUsers.value = [
      { id: 4, email: 'newuser@example.com', user_type: 'buyer', is_verified: true },
      { id: 5, email: 'seller2@example.com', user_type: 'seller', is_verified: false },
      { id: 6, email: 'buyer2@example.com', user_type: 'buyer', is_verified: true }
    ]
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.admin-dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 30px;
  color: #303133;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  border-left: 4px solid;
}

.stat-card.stat-users {
  border-left-color: #409eff;
}

.stat-card.stat-products {
  border-left-color: #67c23a;
}

.stat-card.stat-orders {
  border-left-color: #e6a23c;
}

.stat-card.stat-revenue {
  border-left-color: #f56c6c;
}

.stat-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.charts-row {
  margin-bottom: 20px;
}

.quick-actions {
  margin-bottom: 20px;
}
</style>
