import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { addToCart, fetchProducts } from '../services/api'

function CustomerDashboard() {
  const [products, setProducts] = useState([])
  const [error, setError] = useState(null)
  const [message, setMessage] = useState(null)
  const navigate = useNavigate()

  const currentUser = useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem('loggedInUser'))
    } catch {
      return null
    }
  }, [])

  useEffect(() => {
    if (!currentUser) {
      navigate('/')
      return
    }

    fetchProducts()
      .then(setProducts)
      .catch((err) => setError(err.message))
  }, [currentUser, navigate])

  const handleAddToCart = async (product) => {
    if (!currentUser) {
      navigate('/')
      return
    }

    try {
      setError(null)
      setMessage(null)
      await addToCart({ user_id: currentUser.id, product_id: product.id, quantity: 1 })
      setMessage(`${product.name} added to cart.`)
    } catch (err) {
      setError(err.message)
    }
  }

  if (!currentUser) {
    return null
  }

  return (
    <div className="container customer-dashboard">
      <div className="customer-toolbar">
        <button type="button" className="secondary-button" onClick={() => navigate('/')}>
          Back to Login
        </button>
        <button type="button" className="primary-button" onClick={() => navigate('/cart')}>
          Go to Cart
        </button>
      </div>

      <h2>Welcome, {currentUser.username}</h2>
      <p>View available products below.</p>
      {message && <p className="success-message">{message}</p>}
      {error && <p className="error">{error}</p>}

      <div className="product-grid">
        {products.map((product) => (
          <div key={product.id} className="product-card">
            <h3>{product.name}</h3>
            <p className="product-rate">${Number(product.rate).toFixed(2)}</p>
            <p className="product-stock">Stock: {product.stock}</p>
            <button type="button" className="primary-button" onClick={() => handleAddToCart(product)}>
              Add to Cart
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default CustomerDashboard
