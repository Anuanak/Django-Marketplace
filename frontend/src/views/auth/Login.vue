<template>
  <div class="login-page">
    <h2>{{ $t('auth.loginTitle') }}</h2>
    
    <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleLogin">
      <el-form-item prop="email">
        <el-input
          v-model="form.email"
          :placeholder="$t('auth.email')"
          size="large"
          prefix-icon="Message"
        />
      </el-form-item>
      
      <el-form-item prop="password">
        <el-input
          v-model="form.password"
          type="password"
          :placeholder="$t('auth.password')"
          size="large"
          prefix-icon="Lock"
          show-password
        />
      </el-form-item>
      
      <el-form-item>
        <el-button
          type="primary"
          size="large"
          style="width: 100%"
          :loading="loading"
          native-type="submit"
        >
          {{ $t('common.login') }}
        </el-button>
      </el-form-item>
    </el-form>
    
    <div class="footer-links">
      <router-link to="/auth/register">
        {{ $t('auth.noAccount') }} {{ $t('common.register') }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const formRef = ref()
const loading = ref(false)
const form = ref({
  email: '',
  password: ''
})

const rules = {
  email: [
    { required: true, message: 'Please input email', trigger: 'blur' },
    { type: 'email', message: 'Please input valid email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' }
  ]
}

async function handleLogin() {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    const result = await authStore.login(form.value)
    loading.value = false
    
    if (result.success) {
      ElMessage.success('Login successful')
      const redirect = route.query.redirect || '/'
      router.push(redirect)
    } else {
      ElMessage.error(result.message || 'Login failed')
    }
  })
}
</script>

<style scoped>
.login-page {
  margin: 0;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.footer-links {
  text-align: center;
  margin-top: 20px;
}

.footer-links a {
  color: #409eff;
  text-decoration: none;
}

.footer-links a:hover {
  text-decoration: underline;
}
</style>
