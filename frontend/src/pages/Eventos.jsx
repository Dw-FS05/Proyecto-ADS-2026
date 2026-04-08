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
      <div className="eventos-hero">
        <div className="eventos-hero-waves" aria-hidden />
        <div className="eventos-hero-content">
          <h1>Siente el ritmo de los mejores eventos</h1>
          <p className="eventos-hero-subtitle">Descubre experiencias inolvidables y reserva tu cupo en un solo clic</p>
        </div>
      </div>
      <section className="eventos-section">
        <h2 className="eventos-section-title">Eventos disponibles</h2>
        <p className="eventos-section-subtitle">Explora y únete a los eventos que te interesen</p>
        <div className="eventos-grid">
          {eventos.map((e) => {
            const cuposRestantes = (e.capacidad_max || 0) - (e.asistentes_actuales || 0)
            const casiLleno = cuposRestantes > 0 && cuposRestantes <= 5
            return (
              <Link key={e.id} to={`/eventos/${e.id}`} className="evento-card">
                <h3>{e.nombre}</h3>
                <div className="evento-meta">
                  <span className="badge">{e.asistentes_actuales} / {e.capacidad_max} cupos</span>
                  {e.fecha && <span className="fecha">{e.fecha}</span>}
                </div>
                <span className="evento-card-cta">Ver evento →</span>
              </Link>
            )
          })}
        </div>
        {eventos.length === 0 && (
          <p className="eventos-empty-message">No hay eventos disponibles</p>
        )}
      </section>
    </div>
  )
}
