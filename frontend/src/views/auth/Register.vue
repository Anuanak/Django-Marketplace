<template>
  <div class="register-page">
    <h2>{{ $t('auth.registerTitle') }}</h2>
    
    <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleRegister">
      <el-form-item prop="email">
        <el-input
          v-model="form.email"
          :placeholder="$t('auth.email')"
          size="large"
          prefix-icon="Message"
        />
      </el-form-item>
      
      <el-form-item prop="first_name">
        <el-input
          v-model="form.first_name"
          :placeholder="$t('auth.firstName')"
          size="large"
          prefix-icon="User"
        />
      </el-form-item>
      
      <el-form-item prop="last_name">
        <el-input
          v-model="form.last_name"
          :placeholder="$t('auth.lastName')"
          size="large"
          prefix-icon="User"
        />
      </el-form-item>
      
      <el-form-item prop="phone_number">
        <el-input
          v-model="form.phone_number"
          :placeholder="$t('auth.phone')"
          size="large"
          prefix-icon="Phone"
        />
      </el-form-item>
      
      <el-form-item prop="user_type">
        <el-select v-model="form.user_type" :placeholder="'User Type'" size="large" style="width: 100%">
          <el-option label="Buyer" value="buyer" />
          <el-option label="Seller" value="seller" />
        </el-select>
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
      
      <el-form-item prop="password2">
        <el-input
          v-model="form.password2"
          type="password"
          :placeholder="$t('auth.confirmPassword')"
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
          {{ $t('common.register') }}
        </el-button>
      </el-form-item>
    </el-form>
    
    <div class="footer-links">
      <router-link to="/auth/login">
        {{ $t('auth.haveAccount') }} {{ $t('common.login') }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref()
const loading = ref(false)
const form = ref({
  email: '',
  first_name: '',
  last_name: '',
  phone_number: '',
  user_type: 'buyer',
  password: '',
  password2: ''
})

const validatePassword2 = (rule, value, callback) => {
  if (value !== form.value.password) {
    callback(new Error('Passwords do not match'))
  } else {
    callback()
  }
}

const rules = {
  email: [
    { required: true, message: 'Please input email', trigger: 'blur' },
    { type: 'email', message: 'Please input valid email', trigger: 'blur' }
  ],
  first_name: [
    { required: true, message: 'Please input first name', trigger: 'blur' }
  ],
  last_name: [
    { required: true, message: 'Please input last name', trigger: 'blur' }
  ],
  user_type: [
    { required: true, message: 'Please select user type', trigger: 'change' }
  ],
  password: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' }
  ],
  password2: [
    { required: true, message: 'Please confirm password', trigger: 'blur' },
    { validator: validatePassword2, trigger: 'blur' }
  ]
}

async function handleRegister() {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    const result = await authStore.register(form.value)
    loading.value = false
    
    if (result.success) {
      ElMessage.success('Registration successful')
      router.push('/')
    } else {
      ElMessage.error(result.message || 'Registration failed')
    }
  })
}
</script>

<style scoped>
.register-page {
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
