import React from 'react';
import './Footer.css';

export const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <p>&copy; 2026 Django Marketplace. All rights reserved.</p>
      <p>Built with Django REST Framework & React</p>
    </footer>
  );
};

export default Footer;
