import React from 'react';
import './Header.css';

interface HeaderProps {
  isLoggedIn: boolean;
  onLogout: () => void;
}

export const Header: React.FC<HeaderProps> = ({ isLoggedIn, onLogout }) => {
  return (
    <header className="header">
      <nav className="navbar">
        <a href="/" className="logo">🛒 Marketplace</a>
        <ul className="nav-links">
          <li><a href="/products">Shop</a></li>
          {isLoggedIn ? (
            <>
              <li><a href="/cart">Cart</a></li>
              <li><a href="/orders">Orders</a></li>
              <li><a href="/dashboard">Dashboard</a></li>
              <li><a href="#" onClick={(e) => { e.preventDefault(); onLogout(); }}>Logout</a></li>
            </>
          ) : (
            <>
              <li><a href="/login">Login</a></li>
              <li><a href="/register">Register</a></li>
            </>
          )}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
