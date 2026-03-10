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
      <h1>Crear evento</h1>
      <form onSubmit={handleSubmit}>
        <label>Nombre *</label>
        <input
          value={form.nombre}
          onChange={(e) => setForm({ ...form, nombre: e.target.value })}
          required
        />
        <label>Descripción</label>
        <textarea
          value={form.descripcion}
          onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
          rows={3}
        />
        <label>Fecha</label>
        <input
          type="date"
          value={form.fecha}
          onChange={(e) => setForm({ ...form, fecha: e.target.value })}
        />
        <label>Capacidad máxima</label>
        <input
          type="number"
          min="1"
          value={form.capacidad_max}
          onChange={(e) => setForm({ ...form, capacidad_max: e.target.value })}
        />
        {error && <p className="error">{error}</p>}
        <div className="form-actions">
          <button type="submit" className="btn btn-primary">Crear</button>
          <button type="button" className="btn btn-ghost" onClick={() => navigate('/eventos')}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  )
}
