import { useState } from 'react'
import { Link, useNavigate, Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { crearUsuario } from '../api'
import CustomSelect from '../components/CustomSelect'
import './Login.css'

export default function Register() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ nombre: '', email: '', password: '', rol: 'asistente' })
  const [error, setError] = useState('')

  if (user) return <Navigate to="/eventos" replace />

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await crearUsuario(form)
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.error || 'Error al registrar')
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
          <h2>Únete</h2>
          <h3>Crear cuenta</h3>
          <p>Regístrate para acceder al sistema de gestión de eventos. Podrás ver eventos disponibles, inscribirte y participar en la plataforma.</p>
        </div>
      </div>
      <div className="auth-form-panel">
        <div className="login-card register-card">
        <h1>Crear cuenta</h1>
        <p className="login-subtitle">Completa el formulario para registrarte</p>
        <form onSubmit={handleSubmit} className="register-form">
          <div className="field">
            <label>Nombre</label>
            <input
              placeholder="Tu nombre"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
              required
            />
          </div>
          <div className="field">
            <label>Email</label>
            <input
              type="email"
              placeholder="tu@email.com"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              required
            />
          </div>
          <div className="field">
            <label>Contraseña</label>
            <input
              type="password"
              placeholder="Contraseña"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
            />
          </div>
          <div className="field">
            <label>Rol</label>
            <CustomSelect
              value={form.rol}
              onChange={(rol) => setForm({ ...form, rol })}
              options={[
                { value: 'asistente', label: 'Asistente' },
                { value: 'admin', label: 'Admin' }
              ]}
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button type="submit">Crear cuenta</button>
        </form>
        <p className="card-footer">
          ¿Ya tienes cuenta? <Link to="/login">Iniciar sesión</Link>
        </p>
      </div>
      </div>
    </div>
  )
}
