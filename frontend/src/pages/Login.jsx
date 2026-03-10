import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useNavigate, Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { login as apiLogin } from '../api'
import './Login.css'

export default function Login() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  if (user) return <Navigate to="/eventos" replace />

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await apiLogin(email, password)
      login(data.token, data.rol)
      navigate('/eventos')
    } catch (err) {
      setError(err.response?.data?.mensaje || 'Error al iniciar sesión')
    }
  }

  return (
    <div className="auth-split">
      <div className="auth-banner">
        <div className="auth-banner-shapes">
          <span className="shape shape-1" />
          <span className="shape shape-2" />
          <span className="shape shape-3" />
          <span className="shape shape-4" />
          <span className="shape shape-5" />
        </div>
        <div className="auth-banner-content">
          <h2>Bienvenido</h2>
          <h3>Gestión de Eventos Empresariales</h3>
          <p>Organiza y administra eventos corporativos de forma eficiente. Registra asistentes, crea nuevos eventos y mantén el control desde un solo lugar.</p>
        </div>
      </div>
      <div className="auth-form-panel">
        <div className="login-card">
          <div className="login-icon">📅</div>
          <h1>Iniciar sesión</h1>
          <p className="login-subtitle">Ingresa tus datos para acceder</p>
          <form onSubmit={handleSubmit}>
            <label>Email</label>
            <input
              type="email"
              placeholder="tu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <label>Contraseña</label>
            <input
              type="password"
              placeholder="Contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {error && <p className="error">{error}</p>}
            <button type="submit">Entrar</button>
          </form>
          <p className="card-footer">
            ¿No tienes cuenta? <Link to="/registro">Crear cuenta</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
