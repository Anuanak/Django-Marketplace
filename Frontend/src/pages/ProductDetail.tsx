import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { API } from '../services/api';
import './ProductDetail.css';

const ProductDetailPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const res = await API.getProduct(id);
        setProduct(res.data);
      } catch (err) {
        console.error('Failed to load product', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  if (loading) return <p>Loading...</p>;
  if (!product) return <p>Product not found.</p>;

  return (
    <div className="container">
      <button onClick={() => navigate(-1)} className="btn btn-secondary">Back</button>
      <h1>{product.name}</h1>
      <div style={{ display: 'flex', gap: 24 }}>
        <div style={{ flex: '0 0 320px' }}>
          {product.images && product.images.length > 0 ? (
            <img src={product.images[0].image} alt={product.name} style={{ width: '100%', borderRadius: 8 }} />
          ) : (
            <div style={{ width: '100%', height: 320, background: '#eee' }} />
          )}
        </div>
        <div style={{ flex: 1 }}>
          <p style={{ fontSize: 20, fontWeight: 700 }}>${product.current_price}</p>
          <p>{product.description}</p>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;
