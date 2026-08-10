import React from 'react'

function ProductForm({ initialData, onSave, buttonLabel }) {
  const [name, setName] = React.useState(initialData?.name || '')
  const [rate, setRate] = React.useState(initialData?.rate || '')
  const [stock, setStock] = React.useState(initialData?.stock || '')

  React.useEffect(() => {
    setName(initialData?.name || '')
    setRate(initialData?.rate || '')
    setStock(initialData?.stock || '')
  }, [initialData])

  const handleSubmit = (event) => {
    event.preventDefault()
    onSave({ name, rate: Number(rate), stock: Number(stock) })
  }

  return (
    <form onSubmit={handleSubmit} className="form-row">
      <label>
        Name
        <input value={name} onChange={(e) => setName(e.target.value)} required />
      </label>
      <label>
        Rate
        <input type="number" value={rate} onChange={(e) => setRate(e.target.value)} required min="0" step="0.01" />
      </label>
      <label>
        Stock
        <input type="number" value={stock} onChange={(e) => setStock(e.target.value)} required min="0" step="1" />
      </label>
      <button type="submit">{buttonLabel}</button>
    </form>
  )
}

export default ProductForm
