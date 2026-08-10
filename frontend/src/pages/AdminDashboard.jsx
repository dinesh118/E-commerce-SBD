import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchProducts, addProduct, updateProduct } from '../services/api'
import ProductList from '../components/ProductList'
import ProductForm from '../components/ProductForm'

function AdminDashboard() {
  const [products, setProducts] = useState([])
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [error, setError] = useState(null)
  const [message, setMessage] = useState(null)
  const navigate = useNavigate()

  const loadProducts = () => {
    setError(null)
    fetchProducts()
      .then(setProducts)
      .catch((err) => setError(err.message))
  }

  useEffect(() => {
    loadProducts()
  }, [])

  const handleSave = async (payload) => {
    try {
      setError(null)
      setMessage(null)

      if (selectedProduct) {
        await updateProduct(selectedProduct.id, payload)
        setMessage('Product updated successfully.')
      } else {
        await addProduct(payload)
        setMessage('Product added successfully.')
      }

      setSelectedProduct(null)
      loadProducts()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="container">
      <button onClick={() => navigate('/')}>Back to Login</button>
      <h2>Admin Dashboard</h2>
      <p>Manage products below. Select a row to edit it.</p>
      {message && <p>{message}</p>}
      {error && <p className="error">{error}</p>}

      <ProductForm
        initialData={selectedProduct}
        onSave={handleSave}
        buttonLabel={selectedProduct ? 'Update Product' : 'Save Product'}
      />

      <div style={{ marginTop: '24px' }}>
        <h3>Existing Products</h3>
        <ProductList products={products} />
        {products.length > 0 && (
          <div style={{ marginTop: '16px' }}>
            <p>Select a product below to edit its details.</p>
            <div className="table">
              {products.map((product) => (
                <div key={product.id} style={{ cursor: 'pointer', padding: '8px', borderBottom: '1px solid #eee' }} onClick={() => setSelectedProduct(product)}>
                  {product.name} — Rate: {product.rate} — Stock: {product.stock}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminDashboard
