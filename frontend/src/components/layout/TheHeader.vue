<template>
  <div class="header">
    <div class="header-container">
      <div class="header-left">
        <router-link to="/" class="logo">
          <h1>🛍️ Marketplace</h1>
        </router-link>
        
        <el-menu
          mode="horizontal"
          :default-active="activeMenu"
          router
          class="main-menu"
        >
          <el-menu-item index="/">{{ $t('nav.home') }}</el-menu-item>
          <el-menu-item index="/products">{{ $t('nav.products') }}</el-menu-item>
          <el-menu-item index="/categories">{{ $t('nav.categories') }}</el-menu-item>
        </el-menu>
      </div>
      
      <div class="header-right">
        <!-- Language Switcher -->
        <el-dropdown @command="changeLanguage" class="lang-switcher">
          <span class="el-dropdown-link">
            {{ currentLanguage.toUpperCase() }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="ru">🇷🇺 Русский</el-dropdown-item>
              <el-dropdown-item command="en">🇬🇧 English</el-dropdown-item>
              <el-dropdown-item command="uk">🇺🇦 Українська</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        
        <!-- Cart -->
        <router-link to="/cart" class="cart-link">
          <el-badge :value="cartStore.totalItems" :hidden="cartStore.totalItems === 0">
            <el-icon :size="24"><ShoppingCart /></el-icon>
          </el-badge>
        </router-link>
        
        <!-- User Menu -->
        <el-dropdown v-if="authStore.isAuthenticated" @command="handleUserCommand">
          <span class="user-dropdown">
            <el-avatar :size="32">
              {{ authStore.user?.email?.charAt(0).toUpperCase() }}
            </el-avatar>
            <span class="balance">{{ authStore.balance }} ₽</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">{{ $t('common.profile') }}</el-dropdown-item>
              <el-dropdown-item command="orders">{{ $t('common.orders') }}</el-dropdown-item>
              <el-dropdown-item command="wishlist">Wishlist</el-dropdown-item>
              <el-dropdown-item command="balance">{{ $t('common.balance') }}</el-dropdown-item>
              <el-dropdown-item v-if="authStore.isSeller" command="seller" divided>
                {{ $t('seller.dashboard') }}
              </el-dropdown-item>
              <el-dropdown-item v-if="authStore.isAdmin" command="admin" divided>
                <el-icon><Setting /></el-icon>
                {{ $t('admin.panel') }}
              </el-dropdown-item>
              <el-dropdown-item command="logout" divided>{{ $t('common.logout') }}</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        
        <div v-else class="auth-links">
          <el-button type="primary" link @click="$router.push('/auth/login')">
            {{ $t('common.login') }}
          </el-button>
          <el-button type="primary" @click="$router.push('/auth/register')">
            {{ $t('common.register') }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const route = useRoute()
const { locale } = useI18n()
const authStore = useAuthStore()
const cartStore = useCartStore()

const activeMenu = computed(() => route.path)
const currentLanguage = computed(() => locale.value)

function changeLanguage(lang) {
  locale.value = lang
  localStorage.setItem('language', lang)
}

async function handleUserCommand(command) {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'orders':
      router.push('/orders')
      break
    case 'wishlist':
      router.push('/wishlist')
      break
    case 'balance':
      router.push('/balance')
      break
    case 'seller':
      router.push('/seller/dashboard')
      break
    case 'admin':
      router.push('/admin/dashboard')
      break
    case 'logout':
      await authStore.logout()
      router.push('/')
      break
  }
}

// Fetch cart if authenticated
if (authStore.isAuthenticated) {
  cartStore.fetchCart()
}
</script>

<style scoped>
.header {
  height: 60px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 30px;
}

.logo {
  text-decoration: none;
  color: inherit;
}

.logo h1 {
  font-size: 24px;
  margin: 0;
  color: #409eff;
}

.main-menu {
  border: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.lang-switcher {
  cursor: pointer;
}

.cart-link {
  color: inherit;
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.balance {
  font-weight: 600;
  color: #67c23a;
}

.auth-links {
  display: flex;
  gap: 10px;
}
</style>
