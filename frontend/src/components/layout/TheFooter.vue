<template>
  <div class="footer">
    <div class="footer-container">
      <div class="footer-section">
        <h4>{{ $t('nav.help') }}</h4>
        <ul>
          <li><a href="#">About Us</a></li>
          <li><a href="#">Contact</a></li>
          <li><a href="#">FAQ</a></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h4>For Buyers</h4>
        <ul>
          <li><a href="#">How to Order</a></li>
          <li><a href="#">Payment Methods</a></li>
          <li><a href="#">Returns</a></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h4>For Sellers</h4>
        <ul>
          <li><a href="#">Start Selling</a></li>
          <li><a href="#">Seller Guide</a></li>
          <li><a href="#">Commission</a></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h4>Social</h4>
        <ul>
          <li><a href="#">VK</a></li>
          <li><a href="#">Telegram</a></li>
          <li><a href="#">Instagram</a></li>
        </ul>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>© 2026 Marketplace. All rights reserved.</p>
    </div>
  </div>
</template>

<style scoped>
.footer {
  background-color: #f8f9fa;
  padding: 40px 0 20px;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
}

.footer-section h4 {
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 600;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section li {
  margin-bottom: 8px;
}

.footer-section a {
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.footer-section a:hover {
  color: #409eff;
}

.footer-bottom {
  text-align: center;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
  color: #999;
  font-size: 14px;
}
</style>
