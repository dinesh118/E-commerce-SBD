import { useState } from 'react'

function Register({ onRegister }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError(null)
    setMessage(null)

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    try {
      await onRegister({ username, password, confirm_password: confirmPassword })
      setMessage('Registration successful. You may now login.')
      setUsername('')
      setPassword('')
      setConfirmPassword('')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <h2>New Customer Registration</h2>
      {message && <p>{message}</p>}
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
        <label>
          Retype Password
          <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
        </label>
        <button type="submit">Register</button>
      </form>
    </div>
  )
}

export default Register
