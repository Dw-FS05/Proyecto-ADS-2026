import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import './Layout.css'
import { useAuth } from '../context/AuthContext'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="layout">
      <nav className="nav">
        <NavLink to="/eventos" className="nav-brand">Eventos</NavLink>
        <div className="nav-links">
          <NavLink to="/eventos">Eventos</NavLink>
          {user?.rol === 'admin' && (
            <>
              <NavLink to="/crear-evento">Crear Evento</NavLink>
              <NavLink to="/admin">Admin</NavLink>
            </>
          )}
          <span className="nav-user">{user?.rol}</span>
          <button onClick={handleLogout} className="btn btn-ghost">Salir</button>
        </div>
      </nav>
      <main className="main">
        <Outlet />
      </main>
    </div>
  )
}
