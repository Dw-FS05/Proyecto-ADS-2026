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
    <div className="login-page">
      <div className="login-card">
        <div className="login-icon">📅</div>
        <h1>Crear cuenta</h1>
        <p className="login-subtitle">Completa el formulario para registrarte</p>
        <form onSubmit={handleSubmit}>
          <label>Nombre</label>
          <input
            placeholder="Tu nombre"
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            required
          />
          <label>Email</label>
          <input
            type="email"
            placeholder="tu@email.com"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
          <label>Contraseña</label>
          <input
            type="password"
            placeholder="Contraseña"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />
          <label>Rol</label>
          <CustomSelect
            value={form.rol}
            onChange={(rol) => setForm({ ...form, rol })}
            options={[
              { value: 'asistente', label: 'Asistente' },
              { value: 'admin', label: 'Admin' }
            ]}
          />
          {error && <p className="error">{error}</p>}
          <button type="submit">Crear cuenta</button>
        </form>
        <p className="card-footer">
          ¿Ya tienes cuenta? <Link to="/login">Iniciar sesión</Link>
        </p>
      </div>
    </div>
  )
}
