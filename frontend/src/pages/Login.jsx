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
    <div className="login-page">
      <div className="login-card">
        <div className="login-icon">📅</div>
        <h1>Gestión de Eventos</h1>
        <p className="login-subtitle">Ingresa tus datos para iniciar sesión</p>
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
  )
}
