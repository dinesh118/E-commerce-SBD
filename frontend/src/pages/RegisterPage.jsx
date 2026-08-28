import { useNavigate } from 'react-router-dom'
import Register from '../components/Register'
import { registerUser } from '../services/api'
import '../styles/login.css'
import { Heart, KeyRound, Sparkles, Star, Sun, Trophy } from 'lucide-react'

function RegisterPage() {
  const navigate = useNavigate()

  const handleRegister = async (payload) => {
    await registerUser(payload)
  }

  return (
    <div className="auth-container register-page">
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
          <Register onRegister={handleRegister} />
          <button type="button" className="register-link back-to-login" onClick={() => navigate('/')}>
            Back to login
          </button>
        </div>
      </main>
    </div>
  )
}

export default RegisterPage
