import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Login from '../components/Login'
import Register from '../components/Register'
import { loginUser, loginAdmin, registerUser } from '../services/api'
import '../styles/login.css'
import { ChevronDown } from 'lucide-react'

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
    <div className="auth-container">
      <div className="auth-card">
        <Login
          onLogin={handleLogin}
          onSwitch={(admin) => {
            setIsAdmin(admin)
            setShowRegister(false)
          }}
          isAdmin={isAdmin}
        />

        {/* Registration Toggle Link */}
        {!isAdmin && (
          <div className="register-toggle">
            <button
              type="button"
              className="register-link"
              onClick={() => setShowRegister((prev) => !prev)}
            >
              {showRegister ? 'Hide Registration' : 'New here? Create an account'}
              <ChevronDown
                size={16}
                style={{
                  transform: showRegister ? 'rotate(180deg)' : 'rotate(0deg)',
                  transition: 'transform 0.3s ease',
                }}
              />
            </button>
          </div>
        )}

        {/* Registration Section */}
        {!isAdmin && (
          <div className={`register-section ${showRegister ? 'expanded' : ''}`}>
            <Register onRegister={handleRegister} />
          </div>
        )}
      </div>
    </div>
  )
}

export default LoginPage

