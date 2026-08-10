import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchProducts } from '../services/api'
import ProductList from '../components/ProductList'

function CustomerDashboard() {
  const [products, setProducts] = useState([])
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchProducts()
      .then(setProducts)
      .catch((err) => setError(err.message))
  }, [])

  return (
    <div className="container">
      <button onClick={() => navigate('/')}>Back to Login</button>
      <h2>Customer Dashboard</h2>
      <p>View available products below.</p>
      {error && <p className="error">{error}</p>}
      <ProductList products={products} />
    </div>
  )
}

export default CustomerDashboard
