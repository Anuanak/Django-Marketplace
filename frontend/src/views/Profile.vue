<template>
  <div class="profile-page">
    <el-row :gutter="20">
      <!-- Sidebar -->
      <el-col :xs="24" :md="6">
        <el-card class="profile-sidebar">
          <div class="profile-avatar">
            <el-avatar :size="100" :src="user?.avatar">
              <el-icon :size="40"><User /></el-icon>
            </el-avatar>
            <h3>{{ user?.first_name }} {{ user?.last_name }}</h3>
            <el-tag :type="userTypeTag">{{ $t(`profile.${user?.user_type}`) }}</el-tag>
          </div>
          
          <el-menu :default-active="activeTab" @select="handleTabChange" class="profile-menu">
            <el-menu-item index="info">
              <el-icon><User /></el-icon>
              <span>{{ $t('profile.personalInfo') }}</span>
            </el-menu-item>
            <el-menu-item index="balance">
              <el-icon><Wallet /></el-icon>
              <span>{{ $t('common.balance') }}</span>
            </el-menu-item>
            <el-menu-item index="orders">
              <el-icon><ShoppingBag /></el-icon>
              <span>{{ $t('common.orders') }}</span>
            </el-menu-item>
            <el-menu-item index="password">
              <el-icon><Lock /></el-icon>
              <span>{{ $t('profile.changePassword') }}</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <!-- Main Content -->
      <el-col :xs="24" :md="18">
        <el-card>
          <!-- Personal Info Tab -->
          <div v-show="activeTab === 'info'">
            <h2>{{ $t('profile.personalInfo') }}</h2>
            <el-form :model="profileForm" label-position="top" :rules="profileRules" ref="profileFormRef">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item :label="$t('profile.firstName')" prop="first_name">
                    <el-input v-model="profileForm.first_name" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item :label="$t('profile.lastName')" prop="last_name">
                    <el-input v-model="profileForm.last_name" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item :label="$t('profile.email')" prop="email">
                <el-input v-model="profileForm.email" disabled />
              </el-form-item>
              
              <el-form-item :label="$t('profile.phone')" prop="phone_number">
                <el-input v-model="profileForm.phone_number" />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="updateProfile" :loading="loading">
                  {{ $t('profile.updateProfile') }}
                </el-button>
              </el-form-item>
            </el-form>
            
            <el-divider />
            
            <div class="account-info">
              <h3>{{ $t('profile.accountSettings') }}</h3>
              <el-descriptions :column="1" border>
                <el-descriptions-item :label="$t('profile.accountType')">
                  <el-tag :type="userTypeTag">{{ $t(`profile.${user?.user_type}`) }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item :label="$t('profile.verificationStatus')">
                  <el-tag :type="user?.is_verified ? 'success' : 'warning'">
                    {{ user?.is_verified ? $t('profile.verified') : $t('profile.notVerified') }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item :label="$t('balance.current')">
                  <strong>{{ formatCurrency(user?.balance) }}</strong>
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>

          <!-- Balance Tab -->
          <div v-show="activeTab === 'balance'">
            <h2>{{ $t('common.balance') }}</h2>
            <el-statistic :value="parseFloat(user?.balance || 0)" :precision="2" prefix="₽" class="balance-stat">
              <template #title>
                <span>{{ $t('balance.current') }}</span>
              </template>
            </el-statistic>
            
            <el-button type="primary" @click="showTopUpDialog = true" class="topup-btn">
              <el-icon><Plus /></el-icon>
              {{ $t('common.topup') }}
            </el-button>
          </div>

          <!-- Orders Tab -->
          <div v-show="activeTab === 'orders'">
            <h2>{{ $t('order.history') }}</h2>
            <el-empty v-if="!orders.length" :description="$t('order.history')" />
            <div v-else>
              <el-table :data="orders" style="width: 100%">
                <el-table-column prop="id" :label="$t('order.number')" width="100" />
                <el-table-column prop="created_at" :label="$t('order.date')" width="180" />
                <el-table-column prop="status" :label="$t('order.status')" width="120">
                  <template #default="{ row }">
                    <el-tag>{{ row.status }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="total_price" :label="$t('order.total')">
                  <template #default="{ row }">
                    {{ formatCurrency(row.total_price) }}
                  </template>
                </el-table-column>
                <el-table-column :label="$t('common.edit')" width="100">
                  <template #default="{ row }">
                    <el-button size="small" @click="goToOrder(row.id)">
                      {{ $t('common.edit') }}
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>

          <!-- Change Password Tab -->
          <div v-show="activeTab === 'password'">
            <h2>{{ $t('profile.changePassword') }}</h2>
            <el-form :model="passwordForm" label-position="top" :rules="passwordRules" ref="passwordFormRef">
              <el-form-item :label="$t('profile.currentPassword')" prop="current_password">
                <el-input v-model="passwordForm.current_password" type="password" show-password />
              </el-form-item>
              
              <el-form-item :label="$t('profile.newPassword')" prop="new_password">
                <el-input v-model="passwordForm.new_password" type="password" show-password />
              </el-form-item>
              
              <el-form-item :label="$t('profile.confirmNewPassword')" prop="confirm_password">
                <el-input v-model="passwordForm.confirm_password" type="password" show-password />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="changePassword" :loading="loading">
                  {{ $t('profile.changePassword') }}
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Top Up Balance Dialog -->
    <el-dialog v-model="showTopUpDialog" :title="$t('balance.topup')" width="500px">
      <el-form :model="topUpForm" label-position="top">
        <el-form-item :label="$t('balance.amount')">
          <el-input-number v-model="topUpForm.amount" :min="1" :max="100000" :step="100" style="width: 100%" />
        </el-form-item>
        <el-radio-group v-model="topUpForm.amount">
          <el-radio :label="500">500 ₽</el-radio>
          <el-radio :label="1000">1000 ₽</el-radio>
          <el-radio :label="5000">5000 ₽</el-radio>
          <el-radio :label="10000">10000 ₽</el-radio>
        </el-radio-group>
      </el-form>
      <template #footer>
        <el-button @click="showTopUpDialog = false">{{ $t('common.cancel') }}</el-button>
        <el-button type="primary" @click="topUpBalance" :loading="loading">
          {{ $t('common.confirm') }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { User, Wallet, ShoppingBag, Lock, Plus } from '@element-plus/icons-vue'
import authService from '@/services/authService'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('info')
const loading = ref(false)
const showTopUpDialog = ref(false)
const orders = ref([])

const user = computed(() => authStore.user)

const profileForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone_number: ''
})

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const topUpForm = ref({
  amount: 1000
})

const profileFormRef = ref()
const passwordFormRef = ref()

const profileRules = {
  first_name: [{ required: true, message: 'Please input first name', trigger: 'blur' }],
  last_name: [{ required: true, message: 'Please input last name', trigger: 'blur' }]
}

const passwordRules = {
  current_password: [{ required: true, message: 'Please input current password', trigger: 'blur' }],
  new_password: [
    { required: true, message: 'Please input new password', trigger: 'blur' },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: 'Please confirm new password', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.new_password) {
          callback(new Error('Passwords do not match'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const userTypeTag = computed(() => {
  const type = user.value?.user_type
  return type === 'seller' ? 'warning' : type === 'admin' ? 'danger' : 'success'
})

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(amount || 0)
}

const handleTabChange = (index) => {
  activeTab.value = index
  if (index === 'orders') {
    fetchOrders()
  }
}

const fetchOrders = async () => {
  // Implement order fetching
  orders.value = []
}

const loadProfile = () => {
  if (user.value) {
    profileForm.value = {
      first_name: user.value.first_name || '',
      last_name: user.value.last_name || '',
      email: user.value.email || '',
      phone_number: user.value.phone_number || ''
    }
  }
}

const updateProfile = async () => {
  await profileFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      await authService.updateProfile(profileForm.value)
      await authStore.fetchProfile()
      ElMessage.success('Profile updated successfully')
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || 'Failed to update profile')
    } finally {
      loading.value = false
    }
  })
}

const changePassword = async () => {
  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      await authService.changePassword({
        old_password: passwordForm.value.current_password,
        new_password: passwordForm.value.new_password
      })
      ElMessage.success('Password changed successfully')
      passwordForm.value = { current_password: '', new_password: '', confirm_password: '' }
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || 'Failed to change password')
    } finally {
      loading.value = false
    }
  })
}

const topUpBalance = async () => {
  loading.value = true
  try {
    // Add balance top-up logic here
    ElMessage.success(`Balance topped up with ${formatCurrency(topUpForm.value.amount)}`)
    showTopUpDialog.value = false
    await authStore.fetchProfile()
  } catch (error) {
    ElMessage.error('Failed to top up balance')
  } finally {
    loading.value = false
  }
}

const goToOrder = (orderId) => {
  router.push(`/orders/${orderId}`)
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-sidebar {
  position: sticky;
  top: 80px;
}

.profile-avatar {
  text-align: center;
  margin-bottom: 20px;
}

.profile-avatar h3 {
  margin: 15px 0 10px;
  font-size: 18px;
}

.profile-menu {
  border: none;
}

.account-info {
  margin-top: 30px;
}

.balance-stat {
  margin: 30px 0;
}

.topup-btn {
  margin-top: 20px;
}

h2 {
  margin-bottom: 25px;
  color: #303133;
}
</style>
