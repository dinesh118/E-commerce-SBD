import { useState } from 'react'
import { User, Lock, Eye, EyeOff, AlertCircle, Loader } from 'lucide-react'

function Login({ onLogin, onSwitch, isAdmin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await onLogin({ username, password })
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Segmented Toggle */}
      <div className="segmented-toggle">
        <button
          type="button"
          className={`toggle-button ${!isAdmin ? 'active' : ''}`}
          onClick={() => onSwitch(false)}
        >
          Customer Login
        </button>
        <button
          type="button"
          className={`toggle-button ${isAdmin ? 'active' : ''}`}
          onClick={() => onSwitch(true)}
        >
          Admin Login
        </button>
      </div>

      {/* Title */}
      <h2>{isAdmin ? 'Admin Login' : 'Customer Login'}</h2>

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <AlertCircle size={20} className="error-icon" />
          <span>{error}</span>
        </div>
      )}

      {/* Login Form */}
      <form onSubmit={handleSubmit} className="auth-form">
        {/* Username Field */}
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <div className="input-wrapper">
            <User size={20} className="input-icon-left" />
            <input
              id="username"
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={loading}
              aria-label="Username"
            />
          </div>
        </div>

        {/* Password Field */}
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <div className="input-wrapper password-wrapper">
            <Lock size={20} className="input-icon-left" />
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
              aria-label="Password"
            />
            <button
              type="button"
              className="input-icon-right"
              onClick={() => setShowPassword(!showPassword)}
              tabIndex={-1}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          </div>
        </div>

        {/* Login Button */}
        <button
          type="submit"
          className={`auth-button ${loading ? 'loading' : ''}`}
          disabled={loading}
        >
          {loading && <Loader size={18} className="spinner" />}
          {!loading && (isAdmin ? 'Admin Login' : 'Customer Login')}
        </button>
      </form>
    </>
  )
}

export default Login

