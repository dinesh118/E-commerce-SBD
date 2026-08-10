import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Login from '../components/Login'
import Register from '../components/Register'
import { loginUser, loginAdmin, registerUser } from '../services/api'

function LoginPage() {
  const [isAdmin, setIsAdmin] = useState(false)
  const [showRegister, setShowRegister] = useState(false)
  const navigate = useNavigate()

  const handleLogin = async (payload) => {
    if (isAdmin) {
      await loginAdmin(payload)
      navigate('/admin')
      return
    }

    await loginUser(payload)
    navigate('/customer')
  }

  const handleRegister = async (payload) => {
    await registerUser(payload)
  }

  return (
    <div className="container">
      <Login onLogin={handleLogin} onSwitch={(admin) => { setIsAdmin(admin); setShowRegister(false) }} isAdmin={isAdmin} />

      {!isAdmin && (
        <div>
          <button type="button" onClick={() => setShowRegister((prev) => !prev)}>
            {showRegister ? 'Hide Registration' : 'New User? Register'}
          </button>
        </div>
      )}

      {showRegister && !isAdmin && <Register onRegister={handleRegister} />}
    </div>
  )
}

export default LoginPage
