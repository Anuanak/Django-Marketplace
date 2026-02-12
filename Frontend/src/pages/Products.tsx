import React, { useState, useEffect } from 'react';
import { API } from '../services/api';
import ProductCard from '../components/ProductCard';
import './Products.css';

interface Product {
  id: number;
  name: string;
  price: number;
  current_price: number;
  is_on_sale: boolean;
  average_rating: number;
  seller: { id: number; store_name: string };
}

interface Category {
  id: number;
  name: string;
}

export const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const params: any = {};
        if (search) params.search = search;
        if (selectedCategory) params.category = selectedCategory;
        
        const res = await API.getProducts(params);
        setProducts(res.data.results || res.data);
      } catch (error) {
        console.error('Failed to fetch products:', error);
      } finally {
        setLoading(false);
      }
    };

    const fetchCategories = async () => {
      try {
        const res = await API.getCategories();
        setCategories(res.data.results || res.data);
      } catch (error) {
        console.error('Failed to fetch categories:', error);
      }
    };

    fetchProducts();
    fetchCategories();
  }, [search, selectedCategory]);

  const handleAddToCart = async (product: Product) => {
    try {
      await API.addToCart(product.id, 1);
      alert(`${product.name} added to cart!`);
    } catch (error) {
      alert('Failed to add to cart. Please login first.');
      window.location.href = '/login';
    }
  };

  return (
    <div className="container">
      <h1>Products</h1>
      
      <div className="filters">
        <input
          type="text"
          placeholder="Search products..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="category-select"
        >
          <option value="">All Categories</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.name}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <p>Loading products...</p>
      ) : products.length === 0 ? (
        <p>No products found.</p>
      ) : (
        <div className="products-grid">
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onAddToCart={handleAddToCart}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductsPage;
