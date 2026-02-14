<template>
  <div class="admin-users">
    <div class="page-header">
      <h1>{{ $t('admin.users') }}</h1>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        {{ $t('admin.createUser') }}
      </el-button>
    </div>
    
    <!-- Filters -->
    <el-card class="filter-card">
      <el-form :inline="true">
        <el-form-item>
          <el-input 
            v-model="filters.search" 
            :placeholder="$t('common.search')" 
            clearable
            @clear="fetchUsers"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-select v-model="filters.user_type" :placeholder="$t('profile.accountType')" clearable>
            <el-option label="Buyer" value="buyer" />
            <el-option label="Seller" value="seller" />
            <el-option label="Admin" value="admin" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-select v-model="filters.is_verified" :placeholder="$t('profile.verificationStatus')" clearable>
            <el-option :label="$t('profile.verified')" :value="true" />
            <el-option :label="$t('profile.notVerified')" :value="false" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="fetchUsers">{{ $t('common.search') }}</el-button>
          <el-button @click="resetFilters">{{ $t('common.cancel') }}</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- Users Table -->
    <el-card>
      <el-table :data="users" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="email" :label="$t('auth.email')" min-width="200" />
        <el-table-column :label="$t('auth.firstName')" min-width="120">
          <template #default="{ row }">
            {{ row.first_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column :label="$t('auth.lastName')" min-width="120">
          <template #default="{ row }">
            {{ row.last_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="user_type" :label="$t('profile.accountType')" width="100">
          <template #default="{ row }">
            <el-tag :type="getUserTypeTag(row.user_type)" size="small">
              {{ row.user_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="balance" :label="$t('common.balance')" width="120">
          <template #default="{ row }">
            {{ formatCurrency(row.balance) }}
          </template>
        </el-table-column>
        <el-table-column prop="is_verified" :label="$t('profile.verified')" width="100" align="center">
          <template #default="{ row }">
            <el-switch v-model="row.is_verified" @change="toggleVerification(row)" />
          </template>
        </el-table-column>
        <el-table-column :label="$t('common.edit')" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editUser(row)">{{ $t('common.edit') }}</el-button>
            <el-button size="small" type="danger" @click="deleteUser(row)">{{ $t('common.delete') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next"
        @size-change="fetchUsers"
        @current-change="fetchUsers"
        class="pagination"
      />
    </el-card>
    
    <!-- Create/Edit Dialog -->
    <el-dialog 
      v-model="showCreateDialog" 
      :title="editingUser ? $t('admin.editUser') : $t('admin.createUser')"
      width="600px"
    >
      <el-form :model="userForm" label-position="top" ref="userFormRef">
        <el-form-item :label="$t('auth.email')" prop="email" required>
          <el-input v-model="userForm.email" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item :label="$t('auth.firstName')" prop="first_name">
              <el-input v-model="userForm.first_name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="$t('auth.lastName')" prop="last_name">
              <el-input v-model="userForm.last_name" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item :label="$t('auth.phone')" prop="phone_number">
          <el-input v-model="userForm.phone_number" />
        </el-form-item>
        
        <el-form-item :label="$t('profile.accountType')" prop="user_type" required>
          <el-select v-model="userForm.user_type" style="width: 100%">
            <el-option label="Buyer" value="buyer" />
            <el-option label="Seller" value="seller" />
            <el-option label="Admin" value="admin" />
          </el-select>
        </el-form-item>
        
        <el-form-item v-if="!editingUser" :label="$t('auth.password')" prop="password" required>
          <el-input v-model="userForm.password" type="password" show-password />
        </el-form-item>
        
        <el-form-item :label="$t('common.balance')" prop="balance">
          <el-input-number v-model="userForm.balance" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="userForm.is_verified">{{ $t('profile.verified') }}</el-checkbox>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showCreateDialog = false">{{ $t('common.cancel') }}</el-button>
        <el-button type="primary" @click="saveUser" :loading="saving">
          {{ $t('common.save') }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import api from '@/services/api'

const loading = ref(false)
const saving = ref(false)
const showCreateDialog = ref(false)
const editingUser = ref(null)
const users = ref([])

const filters = reactive({
  search: '',
  user_type: '',
  is_verified: null
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const userForm = ref({
  email: '',
  first_name: '',
  last_name: '',
  phone_number: '',
  user_type: 'buyer',
  password: '',
  balance: 0,
  is_verified: false
})

const userFormRef = ref()

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(amount || 0)
}

const getUserTypeTag = (type) => {
  const types = {
    buyer: 'success',
    seller: 'warning',
    admin: 'danger'
  }
  return types[type] || 'info'
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }
    
    // Add search filter
    if (filters.search) {
      params.search = filters.search
    }
    
    // Add user_type filter
    if (filters.user_type) {
      params.user_type = filters.user_type
    }
    
    // Add is_verified filter
    if (filters.is_verified !== null && filters.is_verified !== '') {
      params.is_verified = filters.is_verified
    }
    
    const response = await api.get('/auth/users/', { params })
    console.log('Users API Response:', response.data)
    
    // Handle different response formats
    if (Array.isArray(response.data)) {
      // Response is a direct array
      users.value = response.data
      pagination.total = response.data.length
    } else if (response.data.results) {
      // Response is paginated with results
      users.value = response.data.results
      pagination.total = response.data.count || 0
    } else if (response.data.data) {
      // Alternative response format
      users.value = Array.isArray(response.data.data) ? response.data.data : []
      pagination.total = response.data.count || response.data.data?.length || 0
    } else {
      // Fallback
      users.value = []
      pagination.total = 0
    }
  } catch (error) {
    console.error('Failed to fetch users:', error.response?.data || error.message)
    users.value = []
    pagination.total = 0
    ElMessage.error(error.response?.data?.detail || 'Failed to fetch users')
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.search = ''
  filters.user_type = ''
  filters.is_verified = null
  fetchUsers()
}

const editUser = (user) => {
  editingUser.value = user
  userForm.value = { ...user }
  showCreateDialog.value = true
}

const saveUser = async () => {
  saving.value = true
  try {
    if (editingUser.value) {
      // Update user
      const updateData = {
        email: userForm.value.email,
        first_name: userForm.value.first_name,
        last_name: userForm.value.last_name,
        phone_number: userForm.value.phone_number,
        user_type: userForm.value.user_type,
        balance: userForm.value.balance,
        is_verified: userForm.value.is_verified
      }
      
      await api.patch(`/auth/users/${editingUser.value.id}/`, updateData)
      ElMessage.success('User updated successfully')
    } else {
      // Create user
      const createData = {
        email: userForm.value.email,
        first_name: userForm.value.first_name,
        last_name: userForm.value.last_name,
        phone_number: userForm.value.phone_number,
        user_type: userForm.value.user_type,
        password: userForm.value.password,
        balance: userForm.value.balance,
        is_verified: userForm.value.is_verified
      }
      
      await api.post('/auth/users/', createData)
      ElMessage.success('User created successfully')
    }
    showCreateDialog.value = false
    editingUser.value = null
    userForm.value = { email: '', first_name: '', last_name: '', phone_number: '', user_type: 'buyer', password: '', balance: 0, is_verified: false }
    fetchUsers()
  } catch (error) {
    console.error('Failed to save user:', error)
    ElMessage.error(error.response?.data?.detail || 'Failed to save user')
  } finally {
    saving.value = false
  }
}

const deleteUser = async (user) => {
  try {
    await ElMessageBox.confirm(
      `Delete user ${user.email}?`,
      'Confirm',
      { type: 'warning' }
    )
    
    await api.delete(`/auth/users/${user.id}/`)
    ElMessage.success('User deleted successfully')
    fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete user:', error)
      ElMessage.error(error.response?.data?.detail || 'Failed to delete user')
    }
  }
}

const toggleVerification = async (user) => {
  try {
    await api.patch(`/auth/users/${user.id}/`, { is_verified: user.is_verified })
    ElMessage.success(`User ${user.is_verified ? 'verified' : 'unverified'}`)
  } catch (error) {
    console.error('Failed to update verification status:', error)
    ElMessage.error('Failed to update verification status')
    user.is_verified = !user.is_verified
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.admin-users {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
}

.filter-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
