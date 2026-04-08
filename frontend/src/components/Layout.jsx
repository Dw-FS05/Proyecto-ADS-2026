import { useState } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import './Layout.css'
import { useAuth } from '../context/AuthContext'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
    setMenuOpen(false)
  }

  return (
    <div className="layout">
      <nav className="nav">
        <NavLink to="/eventos" className="nav-brand" onClick={() => setMenuOpen(false)} end>
          <img src="/logo-eventum.png" alt="eventum" className="nav-brand-logo" />
        </NavLink>
        <button
          type="button"
          className="nav-toggle"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label={menuOpen ? 'Cerrar menú' : 'Abrir menú'}
          aria-expanded={menuOpen}
        >
          <span />
          <span />
          <span />
        </button>
        <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
          <NavLink to="/eventos" onClick={() => setMenuOpen(false)}>Inicio</NavLink>
          <NavLink to="/crear-evento" onClick={() => setMenuOpen(false)}>Crear Evento</NavLink>
          {user?.rol === 'admin' && (
            <NavLink to="/admin" onClick={() => setMenuOpen(false)}>Admin</NavLink>
          )}
          <span className="nav-user">{user?.rol}</span>
          <button onClick={handleLogout} className="btn btn-ghost">Salir</button>
        </div>
      </nav>
      {menuOpen && (
        <div className="nav-overlay" onClick={() => setMenuOpen(false)} aria-hidden="true" />
      )}
      <main className="main">
        <Outlet />
      </main>
    </div>
  )
}
