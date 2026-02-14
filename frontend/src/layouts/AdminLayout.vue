<template>
  <div class="admin-layout">
    <el-container>
      <el-aside width="250px" class="admin-sidebar">
        <div class="admin-menu">
          <div class="admin-logo">
            <el-icon :size="32"><Setting /></el-icon>
            <h3>{{ $t('admin.panel') }}</h3>
          </div>
          <el-menu
            :default-active="activeMenu"
            router
            @select="handleMenuSelect"
          >
            <el-menu-item index="/admin/dashboard">
              <el-icon><DataAnalysis /></el-icon>
              <span>{{ $t('admin.dashboard') }}</span>
            </el-menu-item>
            <el-menu-item index="/admin/users">
              <el-icon><User /></el-icon>
              <span>{{ $t('admin.users') }}</span>
            </el-menu-item>
            <el-menu-item index="/admin/products">
              <el-icon><Box /></el-icon>
              <span>{{ $t('admin.products') }}</span>
            </el-menu-item>
            <el-menu-item index="/admin/categories">
              <el-icon><FolderOpened /></el-icon>
              <span>{{ $t('admin.categories') }}</span>
            </el-menu-item>
            <el-menu-item index="/admin/orders">
              <el-icon><Document /></el-icon>
              <span>{{ $t('admin.orders') }}</span>
            </el-menu-item>
            <el-menu-item index="/admin/reviews">
              <el-icon><Star /></el-icon>
              <span>{{ $t('admin.reviews') }}</span>
            </el-menu-item>
            <el-menu-item index="/admin/keys">
              <el-icon><Key /></el-icon>
              <span>{{ $t('admin.digitalKeys') }}</span>
            </el-menu-item>
            <el-menu-item index="/admin/payments">
              <el-icon><Money /></el-icon>
              <span>{{ $t('admin.payments') }}</span>
            </el-menu-item>
            <el-divider style="background-color: rgba(255,255,255,0.2)" />
            <el-menu-item index="/">
              <el-icon><House /></el-icon>
              <span>{{ $t('nav.home') }}</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-aside>
      
      <el-container>
        <el-header class="admin-header">
          <TheHeader />
        </el-header>
        
        <el-main class="admin-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  DataAnalysis, User, Box, FolderOpened, Document, 
  Star, Key, Money, House, Setting 
} from '@element-plus/icons-vue'
import TheHeader from '@/components/layout/TheHeader.vue'

const route = useRoute()
const activeMenu = computed(() => route.path)

function handleMenuSelect(index) {
  console.log('Admin menu selected:', index)
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
}

.admin-sidebar {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.admin-menu {
  padding: 20px;
}

.admin-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255,255,255,0.2);
}

.admin-logo h3 {
  color: white;
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.admin-header {
  background-color: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  padding: 0;
  z-index: 100;
}

.admin-main {
  background-color: #f0f2f5;
  min-height: calc(100vh - 60px);
  padding: 24px;
}

:deep(.el-menu) {
  background-color: transparent;
  border: none;
}

:deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.85);
  border-radius: 8px;
  margin-bottom: 4px;
}

:deep(.el-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
}

:deep(.el-menu-item.is-active) {
  background-color: rgba(255, 255, 255, 0.25);
  color: white;
}

:deep(.el-divider) {
  margin: 16px 0;
}
</style>
