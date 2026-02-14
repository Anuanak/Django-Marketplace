<template>
  <div class="admin-payments">
    <h1>{{ $t('admin.payments') }}</h1>
    
    <el-card>
      <el-table :data="payments" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="user" label="User" min-width="150" />
        <el-table-column prop="order_id" label="Order" width="100" />
        <el-table-column prop="amount" :label="$t('balance.amount')" width="120">
          <template #default="{ row }">
            {{ formatCurrency(row.amount) }}
          </template>
        </el-table-column>
        <el-table-column prop="payment_method" label="Method" width="120" />
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
const payments = ref([])

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(amount || 0)
}

const getStatusType = (status) => {
  const types = { pending: 'warning', completed: 'success', failed: 'danger' }
  return types[status] || 'info'
}
</script>
