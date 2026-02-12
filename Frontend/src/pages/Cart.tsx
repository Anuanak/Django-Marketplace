import React, { useState, useEffect } from 'react';
import { API } from '../services/api';

export const CartPage: React.FC = () => {
  const [cart, setCart] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const res = await API.getCart();
        setCart(res.data);
      } catch (error) {
        console.error('Failed to fetch cart:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, []);

  const handleRemoveItem = async (itemId: number) => {
    try {
      await API.removeFromCart(itemId);
      if (cart) {
        setCart({
          ...cart,
          items: cart.items.filter((item: any) => item.id !== itemId),
        });
      }
    } catch (error) {
      alert('Failed to remove item');
    }
  };

  if (loading) return <p>Loading cart...</p>;

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <h1>Shopping Cart</h1>

      {!cart || !cart.items || cart.items.length === 0 ? (
        <p>Your cart is empty. <a href="/products">Continue shopping</a></p>
      ) : (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '30px' }}>
            <div>
              {cart.items.map((item: any) => (
                <div
                  key={item.id}
                  style={{
                    background: 'white',
                    padding: '20px',
                    marginBottom: '15px',
                    borderRadius: '8px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <div>
                    <h3>{item.product.name}</h3>
                    <p>${item.product.current_price}</p>
                  </div>
                  <div>
                    <p>Qty: {item.quantity}</p>
                  </div>
                  <button
                    onClick={() => handleRemoveItem(item.id)}
                    style={{
                      background: '#e74c3c',
                      color: 'white',
                      padding: '8px 16px',
                      border: 'none',
                      borderRadius: '5px',
                      cursor: 'pointer',
                    }}
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>

            <div style={{ background: 'white', padding: '20px', borderRadius: '8px', height: 'fit-content' }}>
              <h3>Order Summary</h3>
              <hr />
              <div style={{ marginBottom: '10px' }}>
                <span>Subtotal: </span>
                <span style={{ float: 'right' }}>${cart.total_price?.toFixed(2)}</span>
              </div>
              <div style={{ marginBottom: '10px' }}>
                <span>Shipping: </span>
                <span style={{ float: 'right' }}>$10.00</span>
              </div>
              <hr />
              <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                <span>Total: </span>
                <span style={{ float: 'right', color: '#27ae60' }}>
                  ${(cart.total_price + 10).toFixed(2)}
                </span>
              </div>
              <a
                href="/checkout"
                style={{
                  display: 'block',
                  marginTop: '20px',
                  padding: '12px',
                  background: '#27ae60',
                  color: 'white',
                  textAlign: 'center',
                  textDecoration: 'none',
                  borderRadius: '5px',
                }}
              >
                Proceed to Checkout
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CartPage;
