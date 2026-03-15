import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getEventos } from '../api'
import { useAuth } from '../context/AuthContext'
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
          <div className="eventos-empty">
            <div className="eventos-empty-decoration">
              <span className="eventos-empty-dot eventos-empty-dot-1" />
              <span className="eventos-empty-dot eventos-empty-dot-2" />
              <span className="eventos-empty-dot eventos-empty-dot-3" />
              <span className="eventos-empty-dot eventos-empty-dot-4" />
              <span className="eventos-empty-dot eventos-empty-dot-5" />
            </div>
            <div className="eventos-empty-icon">
              <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
                <rect x="8" y="12" width="48" height="40" rx="8" stroke="currentColor" strokeWidth="2" fill="none" opacity="0.3" />
                <path d="M8 24h48" stroke="currentColor" strokeWidth="2" strokeLinecap="round" opacity="0.5" />
                <circle cx="20" cy="34" r="3" fill="currentColor" opacity="0.6" />
                <circle cx="32" cy="34" r="3" fill="currentColor" opacity="0.6" />
                <circle cx="44" cy="34" r="3" fill="currentColor" opacity="0.6" />
                <path d="M24 48h16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.4" />
              </svg>
            </div>
            <h3 className="eventos-empty-title">Aún no hay eventos</h3>
            <p className="eventos-empty-text">Sé el primero en crear uno y comparte experiencias increíbles con otros.</p>
            <Link to="/crear-evento" className="eventos-empty-cta">Crear evento</Link>
          </div>
        )}
      </section>
    </div>
  )
}
