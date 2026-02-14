<template>
  <div class="admin-orders">
    <h1>{{ $t('admin.orders') }}</h1>
    
    <el-card>
      <el-table :data="orders" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="customer" label="Customer" min-width="150" />
        <el-table-column prop="items_count" label="Items" width="80" align="center" />
        <el-table-column prop="total" :label="$t('order.total')" width="120">
          <template #default="{ row }">
            {{ formatCurrency(row.total) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" :label="$t('order.status')" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" :label="$t('order.date')" width="180" />
        <el-table-column :label="$t('common.edit')" width="120">
          <template #default="{ row }">
            <el-button size="small">{{ $t('common.edit') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)
const orders = ref([])

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(amount || 0)
}

const getStatusType = (status) => {
  const types = { pending: 'warning', processing: 'info', completed: 'success', cancelled: 'danger' }
  return types[status] || 'info'
}
</script>
