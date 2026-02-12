import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { API } from '../services/api';
import './ProductCard.css';

interface Product {
  id: number;
  name: string;
  price: number;
  current_price: number;
  is_on_sale: boolean;
  average_rating: number;
  seller: { id: number; store_name: string };
  image?: string;
}

interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onAddToCart,
}) => {
  return (
    <div className="product-card">
      <div className="product-image">
        {product.image && <img src={product.image} alt={product.name} />}
      </div>
      <h3>{product.name}</h3>
      <p className="seller">{product.seller.store_name}</p>
      <div className="price-section">
        {product.is_on_sale ? (
          <>
            <span className="original-price">${product.price}</span>
            <span className="sale-price">${product.current_price}</span>
            <span className="badge">Sale</span>
          </>
        ) : (
          <span className="price">${product.current_price}</span>
        )}
      </div>
      <p className="rating">⭐ {product.average_rating || 'No ratings'}</p>
      <button
        className="btn btn-primary"
        onClick={() => onAddToCart(product)}
      >
        Add to Cart
      </button>
      <Link to={`/products/${product.id}`} className="btn btn-secondary">
        View Details
      </Link>
    </div>
  );
};

export default ProductCard;
