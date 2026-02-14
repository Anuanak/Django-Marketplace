<template>
  <div class="admin-keys">
    <h1>{{ $t('admin.digitalKeys') }}</h1>
    
    <el-card>
      <el-table :data="keys" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="product" :label="$t('product.name')" min-width="150" />
        <el-table-column prop="key" label="Key" min-width="200" />
        <el-table-column prop="status" :label="$t('order.status')" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === 'available' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="order_id" label="Order" width="100" />
        <el-table-column :label="$t('common.edit')" width="100">
          <template #default="{ row }">
            <el-button size="small" type="danger">{{ $t('common.delete') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)
const keys = ref([])
</script>
