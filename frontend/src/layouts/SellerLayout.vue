<template>
  <div class="seller-layout">
    <el-container>
      <el-aside width="250px" class="seller-sidebar">
        <div class="seller-menu">
          <h3>{{ $t('seller.dashboard') }}</h3>
          <el-menu
            :default-active="activeMenu"
            router
            @select="handleMenuSelect"
          >
            <el-menu-item index="/seller/dashboard">
              <el-icon><DataAnalysis /></el-icon>
              <span>{{ $t('seller.dashboard') }}</span>
            </el-menu-item>
            <el-menu-item index="/seller/products">
              <el-icon><Box /></el-icon>
              <span>{{ $t('seller.products') }}</span>
            </el-menu-item>
            <el-menu-item index="/seller/orders">
              <el-icon><Document /></el-icon>
              <span>{{ $t('seller.orders') }}</span>
            </el-menu-item>
            <el-menu-item index="/seller/keys">
              <el-icon><Key /></el-icon>
              <span>Digital Keys</span>
            </el-menu-item>
            <el-menu-item index="/">
              <el-icon><House /></el-icon>
              <span>{{ $t('nav.home') }}</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-aside>
      
      <el-container>
        <el-header class="seller-header">
          <TheHeader />
        </el-header>
        
        <el-main class="seller-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TheHeader from '@/components/layout/TheHeader.vue'

const route = useRoute()
const activeMenu = computed(() => route.path)

function handleMenuSelect(index) {
  console.log('Menu selected:', index)
}
</script>

<style scoped>
.seller-layout {
  min-height: 100vh;
}

.seller-sidebar {
  background-color: #1f2937;
  color: white;
}

.seller-menu {
  padding: 20px;
}

.seller-menu h3 {
  color: white;
  margin-bottom: 20px;
  font-size: 18px;
}

.seller-header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 0;
}

.seller-main {
  background-color: #f5f5f5;
  min-height: calc(100vh - 60px);
  padding: 24px;
}

:deep(.el-menu) {
  background-color: transparent;
  border: none;
}

:deep(.el-menu-item) {
  color: #d1d5db;
}

:deep(.el-menu-item:hover),
:deep(.el-menu-item.is-active) {
  background-color: #374151 !important;
  color: white;
}
</style>
