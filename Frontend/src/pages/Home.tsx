import React from 'react';

export const HomePage: React.FC = () => {
  return (
    <div style={{ textAlign: 'center', padding: '60px 20px' }}>
      <h1 style={{ fontSize: '48px', marginBottom: '20px' }}>Welcome to Django Marketplace React</h1>
      <p style={{ fontSize: '18px', marginBottom: '30px' }}>
        Shop from multiple sellers, all in one place!
      </p>
      <a href="/products" style={{
        padding: '15px 30px',
        fontSize: '18px',
        backgroundColor: '#3498db',
        color: 'white',
        textDecoration: 'none',
        borderRadius: '5px'
      }}>
        Start Shopping
      </a>
    </div>
  );
};

export default HomePage;
