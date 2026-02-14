<template>
  <div class="admin-categories">
    <div class="page-header">
      <h1>{{ $t('admin.categories') }}</h1>
      <el-button type="primary" @click="showDialog = true">
        <el-icon><Plus /></el-icon>
        {{ $t('admin.createCategory') }}
      </el-button>
    </div>
    
    <el-card>
      <el-table :data="categories" v-loading="loading" stripe row-key="id" default-expand-all>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" :label="$t('product.name')" min-width="200" />
        <el-table-column prop="slug" label="Slug" width="200" />
        <el-table-column prop="product_count" label="Products" width="100" align="center" />
        <el-table-column :label="$t('common.edit')" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small">{{ $t('common.edit') }}</el-button>
            <el-button size="small" type="danger">{{ $t('common.delete') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog v-model="showDialog" :title="$t('admin.createCategory')" width="500px">
      <el-form :model="categoryForm" label-position="top">
        <el-form-item label="Name" required>
          <el-input v-model="categoryForm.name" />
        </el-form-item>
        <el-form-item label="Slug" required>
          <el-input v-model="categoryForm.slug" />
        </el-form-item>
        <el-form-item label="Parent Category">
          <el-select v-model="categoryForm.parent" clearable style="width: 100%">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showDialog = false">{{ $t('common.cancel') }}</el-button>
        <el-button type="primary">{{ $t('common.save') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

const loading = ref(false)
const showDialog = ref(false)
const categories = ref([])
const categoryForm = ref({ name: '', slug: '', parent: null })
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
