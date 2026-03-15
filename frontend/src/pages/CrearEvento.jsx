import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { crearEvento } from '../api'
import './CrearEvento.css'

export default function CrearEvento() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ nombre: '', descripcion: '', fecha: '', capacidad_max: '' })
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const data = {
        nombre: form.nombre,
        descripcion: form.descripcion || null,
        fecha: form.fecha || null,
        capacidad_max: form.capacidad_max ? parseInt(form.capacidad_max) : null
      }
      await crearEvento(data)
      navigate('/eventos')
    } catch (err) {
      setError(err.response?.data?.error || 'Error al crear evento')
    }
  }

  return (
    <div className="crear-evento">
      <div className="crear-evento-card">
        <div className="crear-evento-header">
          <h1>Crear evento</h1>
          <p className="crear-evento-subtitle">Organiza tu próxima fiesta o evento. Reservas en un clic.</p>
        </div>
        <form onSubmit={handleSubmit} className="crear-evento-form">
          <div className="form-grid">
            <div className="form-field">
              <label>Nombre *</label>
              <input
                value={form.nombre}
                onChange={(e) => setForm({ ...form, nombre: e.target.value })}
                required
              />
            </div>
            <div className="form-field">
              <label>Descripción</label>
              <textarea
                value={form.descripcion}
                onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
                rows={2}
              />
            </div>
            <div className="form-field">
              <label>Fecha</label>
              <input
                type="date"
                value={form.fecha}
                onChange={(e) => setForm({ ...form, fecha: e.target.value })}
              />
            </div>
            <div className="form-field">
              <label>Capacidad máxima</label>
              <input
                type="number"
                min="1"
                value={form.capacidad_max}
                onChange={(e) => setForm({ ...form, capacidad_max: e.target.value })}
              />
            </div>
          </div>
        {error && <p className="error">{error}</p>}
        <div className="form-actions">
          <button type="submit" className="btn btn-primary">Crear</button>
          <button type="button" className="btn btn-ghost" onClick={() => navigate('/eventos')}>
            Cancelar
          </button>
        </div>
      </form>
      </div>
    </div>
  )
}
