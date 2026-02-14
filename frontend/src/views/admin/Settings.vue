<template>
  <div class="admin-settings">
    <div class="page-header">
      <h1>{{ $t('admin.settings') }}</h1>
    </div>

    <el-tabs>
      <!-- General Settings -->
      <el-tab-pane :label="$t('admin.generalSettings')">
        <el-card class="settings-card">
          <template #header>
            <span>{{ $t('admin.marketplace') }}</span>
          </template>

          <el-form :model="settings.general" label-width="200px">
            <el-form-item label="Store Name">
              <el-input v-model="settings.general.store_name" placeholder="Your store name" />
            </el-form-item>

            <el-form-item label="Store Description">
              <el-input
                v-model="settings.general.store_description"
                type="textarea"
                rows="3"
                placeholder="Short description of your marketplace"
              />
            </el-form-item>

            <el-form-item label="Support Email">
              <el-input v-model="settings.general.support_email" placeholder="support@example.com" />
            </el-form-item>

            <el-form-item label="Currency">
              <el-select v-model="settings.general.currency" placeholder="Select currency">
                <el-option label="RUB (₽)" value="RUB" />
                <el-option label="USD ($)" value="USD" />
                <el-option label="EUR (€)" value="EUR" />
              </el-select>
            </el-form-item>

            <el-form-item label="Tax Rate (%)">
              <el-input-number
                v-model="settings.general.tax_rate"
                :min="0"
                :max="100"
                :step="0.01"
                placeholder="0.00"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveSettings">{{ $t('common.save') }}</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- Commission Settings -->
      <el-tab-pane :label="$t('admin.commission')">
        <el-card class="settings-card">
          <template #header>
            <span>{{ $t('admin.commissionSettings') }}</span>
          </template>

          <el-form :model="settings.commission" label-width="200px">
            <el-form-item label="Seller Commission (%)">
              <el-input-number
                v-model="settings.commission.seller_commission"
                :min="0"
                :max="100"
                :step="0.01"
                placeholder="15.00"
              />
            </el-form-item>

            <el-form-item label="Digital Product Commission (%)">
              <el-input-number
                v-model="settings.commission.digital_commission"
                :min="0"
                :max="100"
                :step="0.01"
                placeholder="30.00"
              />
            </el-form-item>

            <el-form-item label="Minimum Withdrawal (RUB)">
              <el-input-number
                v-model="settings.commission.min_withdrawal"
                :min="100"
                :step="100"
                placeholder="1000"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveSettings">{{ $t('common.save') }}</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- Email Settings -->
      <el-tab-pane :label="$t('admin.emailSettings')">
        <el-card class="settings-card">
          <template #header>
            <span>{{ $t('admin.smtpConfiguration') }}</span>
          </template>

          <el-form :model="settings.email" label-width="200px">
            <el-form-item label="SMTP Host">
              <el-input v-model="settings.email.smtp_host" placeholder="smtp.gmail.com" />
            </el-form-item>

            <el-form-item label="SMTP Port">
              <el-input-number v-model="settings.email.smtp_port" :min="1" placeholder="587" />
            </el-form-item>

            <el-form-item label="SMTP Email">
              <el-input v-model="settings.email.smtp_email" placeholder="noreply@example.com" />
            </el-form-item>

            <el-form-item label="SMTP Password">
              <el-input
                v-model="settings.email.smtp_password"
                type="password"
                placeholder="••••••••"
              />
            </el-form-item>

            <el-form-item label="Use TLS">
              <el-switch v-model="settings.email.use_tls" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveSettings">{{ $t('common.save') }}</el-button>
              <el-button @click="testEmail">{{ $t('admin.testEmail') }}</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- Payment Settings -->
      <el-tab-pane :label="$t('admin.paymentSettings')">
        <el-card class="settings-card">
          <template #header>
            <span>{{ $t('admin.paymentMethods') }}</span>
          </template>

          <el-form :model="settings.payment" label-width="200px">
            <el-form-item label="Stripe Enabled">
              <el-switch v-model="settings.payment.stripe_enabled" />
            </el-form-item>

            <el-form-item label="Stripe Public Key">
              <el-input
                v-model="settings.payment.stripe_public_key"
                placeholder="pk_live_..."
              />
            </el-form-item>

            <el-form-item label="Stripe Secret Key">
              <el-input
                v-model="settings.payment.stripe_secret_key"
                type="password"
                placeholder="sk_live_..."
              />
            </el-form-item>

            <el-form-item label="PayPal Enabled">
              <el-switch v-model="settings.payment.paypal_enabled" />
            </el-form-item>

            <el-form-item label="PayPal Client ID">
              <el-input v-model="settings.payment.paypal_client_id" placeholder="Your Client ID" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveSettings">{{ $t('common.save') }}</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- Notification Settings -->
      <el-tab-pane :label="$t('admin.notificationSettings')">
        <el-card class="settings-card">
          <template #header>
            <span>{{ $t('admin.notifications') }}</span>
          </template>

          <el-form :model="settings.notifications" label-width="200px">
            <el-form-item label="Email Notifications">
              <el-switch v-model="settings.notifications.email_enabled" />
            </el-form-item>

            <el-form-item label="Order Notifications">
              <el-switch v-model="settings.notifications.order_enabled" />
            </el-form-item>

            <el-form-item label="Review Notifications">
              <el-switch v-model="settings.notifications.review_enabled" />
            </el-form-item>

            <el-form-item label="Seller Report Interval">
              <el-select v-model="settings.notifications.report_interval" placeholder="Select interval">
                <el-option label="Daily" value="daily" />
                <el-option label="Weekly" value="weekly" />
                <el-option label="Monthly" value="monthly" />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveSettings">{{ $t('common.save') }}</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const settings = ref({
  general: {
    store_name: 'Django Marketplace',
    store_description: 'Premium online marketplace',
    support_email: 'support@example.com',
    currency: 'RUB',
    tax_rate: 18.00
  },
  commission: {
    seller_commission: 15.00,
    digital_commission: 30.00,
    min_withdrawal: 1000
  },
  email: {
    smtp_host: 'smtp.gmail.com',
    smtp_port: 587,
    smtp_email: 'noreply@marketplace.com',
    smtp_password: '',
    use_tls: true
  },
  payment: {
    stripe_enabled: true,
    stripe_public_key: '',
    stripe_secret_key: '',
    paypal_enabled: false,
    paypal_client_id: ''
  },
  notifications: {
    email_enabled: true,
    order_enabled: true,
    review_enabled: true,
    report_interval: 'weekly'
  }
})

const saveSettings = () => {
  // TODO: Implement API call to save settings
  ElMessage.success('Settings saved successfully')
}

const testEmail = () => {
  // TODO: Implement email test
  ElMessage.info('Test email sent')
}

onMounted(() => {
  // TODO: Load settings from API
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
}

.settings-card {
  margin-bottom: 20px;
}

.el-tabs {
  margin-top: 20px;
}
</style>
