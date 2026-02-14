<template>
  <div class="not-found">
    <el-result
      icon="error"
      title="404"
      sub-title="Page not found"
    >
      <template #extra>
        <el-button type="primary" @click="$router.push('/')">
          Back to Home
        </el-button>
      </template>
    </el-result>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}
</style>
