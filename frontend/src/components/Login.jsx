import { useState } from 'react'

function Login({ onLogin, onSwitch, isAdmin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError(null)
    try {
      await onLogin({ username, password })
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <div className="nav-buttons">
        <button type="button" onClick={() => onSwitch(false)} disabled={!isAdmin}>
          Customer Login
        </button>
        <button type="button" onClick={() => onSwitch(true)} disabled={isAdmin}>
          Admin Login
        </button>
      </div>

      <h2>{isAdmin ? 'Admin Login' : 'Customer Login'}</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit} className="form-row">
        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} required />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        <button type="submit">Login</button>
      </form>
    </div>
  )
}

export default Login
