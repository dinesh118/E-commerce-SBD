import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Login from '../components/Login'
import { loginUser, loginAdmin } from '../services/api'
import '../styles/login.css'
import { Heart, KeyRound, Sparkles, Star, Sun, Trophy } from 'lucide-react'

function LoginPage() {
  const [isAdmin, setIsAdmin] = useState(false)
  const navigate = useNavigate()

  const handleLogin = async (payload) => {
    if (isAdmin) {
      await loginAdmin(payload)
      navigate('/admin')
      return
    }

    const user = await loginUser(payload)
    localStorage.setItem('loggedInUser', JSON.stringify(user))
    navigate('/customer')
  }

  return (
    <div className="auth-container">
      <section className="wish-art" aria-hidden="true">
        <p className="wish-art-intro">Be careful what<br /><em>you wish for</em></p>
        <div className="wish-brand-mark">ONE WISH WILLOW</div>
        <div className="wish-grid">
          <div className="wish-tile"><span>1. WISH TO<br />BE FAMOUS</span><Trophy /></div>
          <div className="wish-tile"><span>2. WISH TO<br />BE RICH</span><Sparkles /></div>
          <div className="wish-tile"><span>3. WISH FOR<br />TRUE LOVE</span><Heart /></div>
          <div className="wish-tile"><span>4. WISH FOR<br />WORLD PEACE</span><Sun /></div>
          <div className="wish-tile"><span>5. BE<br />CAREFUL</span><Star /></div>
          <div className="wish-tile"><span>6. WISH TO<br />BE BETTER</span><KeyRound /></div>
        </div>
      </section>
      <main className="auth-panel-right">
        <div className="auth-card">
          <Login
          onLogin={handleLogin}
          onSwitch={(admin) => {
            setIsAdmin(admin)
          }}
          isAdmin={isAdmin}
          />

          {!isAdmin && (
            <div className="register-toggle">
              <button type="button" className="register-link" onClick={() => navigate('/register')}>
                New here? Create an account
              </button>
            </div>
          )}
        </div>
      </main>
      </div>
  )
}

export default LoginPage

