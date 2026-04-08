import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Eventos from './pages/Eventos'
import EventoDetalle from './pages/EventoDetalle'
import CrearEvento from './pages/CrearEvento'
import Admin from './pages/Admin'

function ProtectedRoute({ children, adminOnly }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (adminOnly && user?.rol !== 'admin') return <Navigate to="/eventos" replace />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/registro" element={<Register />} />
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/eventos" replace />} />
        <Route path="eventos" element={
          <ProtectedRoute><Eventos /></ProtectedRoute>
        } />
        <Route path="eventos/:id" element={
          <ProtectedRoute><EventoDetalle /></ProtectedRoute>
        } />
        <Route path="crear-evento" element={
          <ProtectedRoute><CrearEvento /></ProtectedRoute>
        } />
        <Route path="admin" element={
          <ProtectedRoute adminOnly><Admin /></ProtectedRoute>
        } />
      </Route>
      <Route path="*" element={<Navigate to="/eventos" replace />} />
    </Routes>
  )
}
