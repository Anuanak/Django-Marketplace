<template>
  <div class="balance-page">
    <div class="container">
      <h1>{{ $t('common.balance') }}</h1>
      
      <el-row :gutter="20">
        <!-- Balance Card -->
        <el-col :xs="24" :md="12">
          <el-card class="balance-card" shadow="always">
            <template #header>
              <div class="balance-header">
                <span>{{ $t('balance.current') }}</span>
                <el-icon :size="24"><Wallet /></el-icon>
              </div>
            </template>
            
            <el-statistic :value="parseFloat(balance)" :precision="2" prefix="₽" class="balance-amount">
              <template #suffix>
                <span class="balance-currency">RUB</span>
              </template>
            </el-statistic>
            
            <el-button 
              type="primary" 
              size="large" 
              style="width: 100%; margin-top: 30px"
              @click="showTopUpDialog = true"
            >
              <el-icon><Plus /></el-icon>
              {{ $t('balance.topup') }}
            </el-button>
          </el-card>
        </el-col>
        
        <!-- Quick Actions -->
        <el-col :xs="24" :md="12">
          <el-card>
            <template #header>
              <span>{{ $t('balance.topup') }}</span>
            </template>
            
            <div class="quick-amounts">
              <el-button 
                v-for="amount in quickAmounts" 
                :key="amount"
                size="large"
                @click="selectAmount(amount)"
                class="amount-btn"
              >
                {{ formatCurrency(amount) }}
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- Transactions History -->
      <el-card class="transactions-card">
        <template #header>
          <div class="transactions-header">
            <span>{{ $t('balance.transactions') }}</span>
            <el-button link @click="fetchTransactions">
              <el-icon><Refresh /></el-icon>
              {{ $t('common.submit') }}
            </el-button>
          </div>
        </template>
        
        <el-table :data="transactions" v-loading="loadingTransactions" stripe>
          <el-table-column prop="id" label="ID" width="80" />
          
          <el-table-column :label="$t('balance.type')" width="150">
            <template #default="{ row }">
              <el-tag :type="getTransactionTypeTag(row.type)">
                {{ $t(`balance.${row.type}`) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="amount" :label="$t('balance.amount')" width="150">
            <template #default="{ row }">
              <span :class="{ 'amount-positive': row.type === 'deposit', 'amount-negative': row.type === 'purchase' }">
                {{ row.type === 'purchase' ? '-' : '+' }}{{ formatCurrency(Math.abs(row.amount)) }}
              </span>
            </template>
          </el-table-column>
          
          <el-table-column prop="description" :label="$t('product.description')" />
          
          <el-table-column prop="created_at" :label="$t('balance.date')" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty v-if="!transactions.length && !loadingTransactions" :description="$t('balance.transactions')" />
      </el-card>
    </div>
    
    <!-- Top Up Dialog -->
    <el-dialog v-model="showTopUpDialog" :title="$t('balance.topup')" width="500px">
      <el-form :model="topUpForm" label-position="top">
        <el-form-item :label="$t('balance.amount')">
          <el-input-number 
            v-model="topUpForm.amount" 
            :min="1" 
            :max="100000" 
            :step="100" 
            size="large"
            style="width: 100%" 
          />
        </el-form-item>
        
        <el-divider />
        
        <div class="preset-amounts">
          <el-button 
            v-for="amount in quickAmounts" 
            :key="amount"
            @click="topUpForm.amount = amount"
            :type="topUpForm.amount === amount ? 'primary' : ''"
          >
            {{ formatCurrency(amount) }}
          </el-button>
        </div>
      </el-form>
      
      <template #footer>
        <el-button @click="showTopUpDialog = false">{{ $t('common.cancel') }}</el-button>
        <el-button type="primary" @click="topUpBalance" :loading="loadingTopUp">
          {{ $t('common.confirm') }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { Wallet, Plus, Refresh } from '@element-plus/icons-vue'
import api from '@/services/api'

const authStore = useAuthStore()

const showTopUpDialog = ref(false)
const loadingTransactions = ref(false)
const loadingTopUp = ref(false)
const transactions = ref([])

const topUpForm = ref({
  amount: 1000
})

const quickAmounts = [500, 1000, 2500, 5000, 10000, 20000]

const balance = computed(() => authStore.user?.balance || '0.00')

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(amount || 0)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getTransactionTypeTag = (type) => {
  const tags = {
    deposit: 'success',
    purchase: 'warning',
    refund: 'info'
  }
  return tags[type] || ''
}

const selectAmount = (amount) => {
  topUpForm.value.amount = amount
  showTopUpDialog.value = true
}

const fetchTransactions = async () => {
  loadingTransactions.value = true
  try {
    // Mock transactions for now
    transactions.value = [
      {
        id: 1,
        type: 'deposit',
        amount: 1000,
        description: 'Balance top-up',
        created_at: new Date().toISOString()
      }
    ]
  } catch (error) {
    console.error('Failed to fetch transactions:', error)
  } finally {
    loadingTransactions.value = false
  }
}

const topUpBalance = async () => {
  if (topUpForm.value.amount < 1) {
    ElMessage.warning('Please enter a valid amount')
    return
  }
  
  loadingTopUp.value = true
  try {
    // Simulate top-up - replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success(`Balance topped up with ${formatCurrency(topUpForm.value.amount)}`)
    showTopUpDialog.value = false
    
    // Refresh user data and transactions
    await authStore.fetchProfile()
    await fetchTransactions()
  } catch (error) {
    ElMessage.error('Failed to top up balance')
  } finally {
    loadingTopUp.value = false
  }
}

onMounted(() => {
  fetchTransactions()
})
</script>

<style scoped>
.balance-page {
  min-height: calc(100vh - 200px);
  padding: 20px;
  background-color: #f5f7fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 30px;
  color: #303133;
}

.balance-card {
  text-align: center;
}

.balance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.balance-amount {
  margin: 30px 0;
}

.balance-currency {
  font-size: 14px;
  color: #909399;
  margin-left: 8px;
}

.quick-amounts {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.amount-btn {
  height: 60px;
  font-size: 18px;
  font-weight: 600;
}

.transactions-card {
  margin-top: 20px;
}

.transactions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.amount-positive {
  color: #67c23a;
  font-weight: 600;
}

.amount-negative {
  color: #f56c6c;
  font-weight: 600;
}

.preset-amounts {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

@media (max-width: 768px) {
  .quick-amounts {
    grid-template-columns: 1fr;
  }
}
</style>
