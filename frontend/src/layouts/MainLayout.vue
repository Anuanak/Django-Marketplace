<template>
  <div class="main-layout">
    <el-container>
      <el-header class="header">
        <TheHeader />
      </el-header>
      
      <el-container>
        <el-aside v-if="showSidebar" width="250px" class="sidebar">
          <TheSidebar />
        </el-aside>
        
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
      
      <el-footer class="footer">
        <TheFooter />
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TheHeader from '@/components/layout/TheHeader.vue'
import TheSidebar from '@/components/layout/TheSidebar.vue'
import TheFooter from '@/components/layout/TheFooter.vue'

const route = useRoute()
const showSidebar = computed(() => {
  // Hide sidebar on certain pages
  return !['checkout', 'cart'].includes(route.name)
})
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  padding: 0;
}

.sidebar {
  background-color: #fff;
  padding: 20px 0;
  height: calc(100vh - 60px - 80px);
  overflow-y: auto;
}

.main-content {
  background-color: #f5f5f5;
  min-height: calc(100vh - 60px - 80px);
  padding: 20px;
}

.footer {
  background-color: #fff;
  border-top: 1px solid #eee;
  padding: 20px;
  height: auto;
}

:deep(.el-header) {
  height: 60px;
  line-height: 60px;
}

:deep(.el-footer) {
  height: auto;
}
</style>
