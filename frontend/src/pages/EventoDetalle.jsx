import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { getEvento, registrarAsistente } from '../api'
import './EventoDetalle.css'

export default function EventoDetalle() {
  const { id } = useParams()
  const { user } = useAuth()
  const [evento, setEvento] = useState(null)
  const [loading, setLoading] = useState(true)
  const [msg, setMsg] = useState('')

  useEffect(() => {
    getEvento(id)
      .then(({ data }) => setEvento(data))
      .catch(() => setEvento(null))
      .finally(() => setLoading(false))
  }, [id])

  const yaInscrito = evento?.asistentes?.some((a) => a.id === user?.id)
  const lleno = evento && evento.asistentes_actuales >= evento.capacidad_max

  const handleRegistrar = async () => {
    setMsg('')
    try {
      await registrarAsistente(id, user.id)
      setMsg('Registro exitoso')
      const { data } = await getEvento(id)
      setEvento(data)
    } catch (err) {
      setMsg(err.response?.data?.error || err.response?.data?.mensaje || 'Error')
    }
  }

  if (loading) return <div className="loading">Cargando...</div>
  if (!evento) return <div className="error-msg">Evento no encontrado</div>

  return (
    <div className="evento-detalle">
      <div className="evento-detalle-card">
        <div className="evento-header">
          <h1>{evento.nombre}</h1>
          {evento.fecha && <span className="fecha">{evento.fecha}</span>}
        </div>
        {evento.descripcion && <p className="descripcion">{evento.descripcion}</p>}
        <div className="evento-acciones">
          <div className="evento-stats">
            <span>{evento.asistentes_actuales} / {evento.capacidad_max} inscritos</span>
          </div>
          {!yaInscrito && !lleno && (
            <button type="button" onClick={handleRegistrar} className="btn btn-primary">Reservar mi lugar</button>
          )}
          {yaInscrito && <p className="inscrito">Ya estás inscrito</p>}
          {lleno && !yaInscrito && <p className="lleno">Evento lleno</p>}
          {msg && <p className={msg.includes('exitoso') ? 'msg-ok' : 'msg-err'}>{msg}</p>}
        </div>
      {evento.asistentes?.length > 0 && (
        <div className="asistentes">
          <h3>Inscritos</h3>
          <ul>
            {evento.asistentes.map((a) => (
              <li key={a.id}>{a.nombre} - {a.email}</li>
            ))}
          </ul>
        </div>
      )}
      </div>
    </div>
  )
}
