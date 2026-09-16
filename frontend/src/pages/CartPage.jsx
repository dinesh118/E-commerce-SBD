import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Minus, Plus, Trash2 } from 'lucide-react'
import { fetchCart, removeCartItem, updateCartItem } from '../services/api'

function CartPage() {
  const navigate = useNavigate()
  const [items, setItems] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const currentUser = useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem('loggedInUser'))
    } catch {
      return null
    }
  }, [])

  const loadCart = async () => {
    if (!currentUser) {
      navigate('/')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const cartItems = await fetchCart(currentUser.id)
      setItems(cartItems)
    } catch (err) {
      setError(err.message || 'Unable to load cart.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadCart()
  }, [currentUser, navigate])

  const handleQuantityChange = async (itemId, nextQuantity) => {
    if (nextQuantity <= 0) {
      await removeCartItem(itemId)
      loadCart()
      return
    }

    try {
      await updateCartItem(itemId, { quantity: nextQuantity })
      loadCart()
    } catch (err) {
      setError(err.message || 'Unable to update quantity.')
    }
  }

  const handleRemove = async (itemId) => {
    try {
      await removeCartItem(itemId)
      loadCart()
    } catch (err) {
      setError(err.message || 'Unable to remove item.')
    }
  }

  const subtotal = items.reduce((sum, item) => sum + item.quantity * item.product_rate, 0)

  if (!currentUser) {
    return null
  }

  return (
    <div className="container cart-page">
      <div className="customer-toolbar">
        <button type="button" className="secondary-button" onClick={() => navigate('/customer')}>
          Continue Shopping
        </button>
      </div>

      <h2>Your Cart</h2>
      <p>Review your selected items before checkout.</p>

      {error && <p className="error">{error}</p>}
      {loading && <p>Loading cart...</p>}

      {!loading && items.length === 0 && (
        <div className="empty-cart">
          <p>Your cart is empty.</p>
          <button type="button" className="primary-button" onClick={() => navigate('/customer')}>
            Shop now
          </button>
        </div>
      )}

      {items.length > 0 && (
        <div className="cart-layout">
          <div className="cart-items">
            {items.map((item) => (
              <div key={item.id} className="cart-item">
                <div>
                  <h3>{item.product_name}</h3>
                  <p>${Number(item.product_rate).toFixed(2)} each</p>
                </div>

                <div className="cart-actions">
                  <div className="quantity-controls">
                    <button type="button" onClick={() => handleQuantityChange(item.id, item.quantity - 1)} aria-label="Decrease quantity">
                      <Minus size={14} />
                    </button>
                    <span>{item.quantity}</span>
                    <button type="button" onClick={() => handleQuantityChange(item.id, item.quantity + 1)} aria-label="Increase quantity">
                      <Plus size={14} />
                    </button>
                  </div>

                  <button type="button" className="remove-button" onClick={() => handleRemove(item.id)}>
                    <Trash2 size={14} /> Remove
                  </button>
                </div>

                <div className="item-total">${(item.quantity * item.product_rate).toFixed(2)}</div>
              </div>
            ))}
          </div>

          <aside className="cart-summary">
            <h3>Order Summary</h3>
            <div className="summary-row">
              <span>Subtotal</span>
              <strong>${subtotal.toFixed(2)}</strong>
            </div>
            <div className="summary-row total-row">
              <span>Total</span>
              <strong>${subtotal.toFixed(2)}</strong>
            </div>
            <button type="button" className="primary-button checkout-button">
              Proceed to Checkout
            </button>
          </aside>
        </div>
      )}
    </div>
  )
}

export default CartPage
