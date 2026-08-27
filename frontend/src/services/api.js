const API_URL = ''

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  })
  const body = await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(body?.detail || body?.message || 'Request failed')
  }
  return body
}

export function registerUser(payload) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function loginUser(payload) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function loginAdmin(payload) {
  return request('/auth/admin-login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function fetchProducts() {
  return request('/products')
}

export function addProduct(payload) {
  return request('/products', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateProduct(productId, payload) {
  return request(`/products/${productId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}
