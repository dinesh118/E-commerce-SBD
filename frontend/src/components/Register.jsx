import { useState } from 'react'
import { User, Lock, Eye, EyeOff, AlertCircle, CheckCircle, Loader } from 'lucide-react'

function Register({ onRegister }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError(null)
    setMessage(null)
    setLoading(true)

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long')
      setLoading(false)
      return
    }

    try {
      await onRegister({ username, password, confirm_password: confirmPassword })
      setMessage('✓ Registration successful! You can now login.')
      setUsername('')
      setPassword('')
      setConfirmPassword('')
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h2>Create Account</h2>

      {/* Success Message */}
      {message && (
        <div className="success-message">
          <CheckCircle size={20} className="success-icon" />
          <span>{message}</span>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <AlertCircle size={20} className="error-icon" />
          <span>{error}</span>
        </div>
      )}

      {/* Registration Form */}
      <form onSubmit={handleSubmit} className="auth-form">
        {/* Username Field */}
        <div className="form-group">
          <label htmlFor="register-username">Username</label>
          <div className="input-wrapper">
            <User size={20} className="input-icon-left" />
            <input
              id="register-username"
              type="text"
              placeholder="Choose a username"
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
          <label htmlFor="register-password">Password</label>
          <div className="input-wrapper password-wrapper">
            <Lock size={20} className="input-icon-left" />
            <input
              id="register-password"
              type={showPassword ? 'text' : 'password'}
              placeholder="Create a password (min 6 chars)"
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

        {/* Confirm Password Field */}
        <div className="form-group">
          <label htmlFor="register-confirm">Confirm Password</label>
          <div className="input-wrapper password-wrapper">
            <Lock size={20} className="input-icon-left" />
            <input
              id="register-confirm"
              type={showConfirmPassword ? 'text' : 'password'}
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={loading}
              aria-label="Confirm Password"
            />
            <button
              type="button"
              className="input-icon-right"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              tabIndex={-1}
              aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
            >
              {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          </div>
        </div>

        {/* Register Button */}
        <button
          type="submit"
          className={`auth-button ${loading ? 'loading' : ''}`}
          disabled={loading}
        >
          {loading && <Loader size={18} className="spinner" />}
          {!loading && 'Create Account'}
        </button>
      </form>
    </>
  )
}

export default Register

