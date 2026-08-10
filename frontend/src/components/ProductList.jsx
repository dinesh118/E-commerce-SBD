function ProductList({ products }) {
  if (!products.length) {
    return <p>No products available.</p>
  }

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Rate</th>
          <th>Stock</th>
        </tr>
      </thead>
      <tbody>
        {products.map((product) => (
          <tr key={product.id}>
            <td>{product.name}</td>
            <td>{product.rate}</td>
            <td>{product.stock}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default ProductList
