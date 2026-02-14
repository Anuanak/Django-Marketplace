<template>
  <div class="auth-layout">
    <div class="auth-container">
      <div class="auth-card">
        <div class="logo-section">
          <h1>🛍️ Marketplace</h1>
          <p>{{ $t('common.welcome') }}</p>
        </div>
        <router-view />
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-container {
  width: 100%;
  max-width: 450px;
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  padding: 40px;
}

.logo-section {
  text-align: center;
  margin-bottom: 30px;
}

.logo-section h1 {
  font-size: 32px;
  margin-bottom: 10px;
  color: #333;
}

.logo-section p {
  color: #666;
  font-size: 14px;
}
</style>
