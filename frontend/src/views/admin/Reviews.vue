<template>
  <div class="admin-reviews">
    <h1>{{ $t('admin.reviews') }}</h1>
    
    <el-card>
      <el-table :data="reviews" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="product" :label="$t('product.name')" min-width="150" />
        <el-table-column prop="user" label="User" width="150" />
        <el-table-column prop="rating" :label="$t('product.rating')" width="120">
          <template #default="{ row }">
            <el-rate v-model="row.rating" disabled show-score />
          </template>
        </el-table-column>
        <el-table-column prop="comment" label="Comment" min-width="200" />
        <el-table-column prop="is_approved" label="Approved" width="100" align="center">
          <template #default="{ row }">
            <el-switch v-model="row.is_approved" />
          </template>
        </el-table-column>
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
const reviews = ref([])
</script>
