import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getEventos } from '../api'
import './Eventos.css'

export default function Eventos() {
  const [eventos, setEventos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getEventos()
      .then(({ data }) => setEventos(data))
      .catch(() => setError('Error al cargar eventos'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="loading">Cargando...</div>
  if (error) return <div className="error-msg">{error}</div>

  return (
    <div className="eventos-page">
      <h1>Eventos disponibles</h1>
      <div className="eventos-grid">
        {eventos.map((e) => (
          <Link key={e.id} to={`/eventos/${e.id}`} className="evento-card">
            <h3>{e.nombre}</h3>
            <div className="evento-meta">
              <span className="badge">{e.asistentes_actuales} / {e.capacidad_max} cupos</span>
              {e.fecha && <span className="fecha">{e.fecha}</span>}
            </div>
          </Link>
        ))}
      </div>
      {eventos.length === 0 && <p className="empty">No hay eventos disponibles</p>}
    </div>
  )
}
