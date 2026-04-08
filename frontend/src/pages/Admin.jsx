import { useState, useEffect } from 'react'
import { getUsuarios, crearUsuario } from '../api'
import CustomSelect from '../components/CustomSelect'
import './Admin.css'

export default function Admin() {
  const [usuarios, setUsuarios] = useState([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({ nombre: '', email: '', password: '', rol: 'asistente' })
  const [msg, setMsg] = useState('')

  useEffect(() => {
    getUsuarios()
      .then(({ data }) => setUsuarios(data))
      .catch(() => setUsuarios([]))
      .finally(() => setLoading(false))
  }, [])

  const handleCrearUsuario = async (e) => {
    e.preventDefault()
    setMsg('')
    try {
      await crearUsuario(form)
      setMsg('Usuario creado')
      setForm({ nombre: '', email: '', password: '', rol: 'asistente' })
      const { data } = await getUsuarios()
      setUsuarios(data)
    } catch (err) {
      setMsg(err.response?.data?.error || 'Error al crear usuario')
    }
  }

  if (loading) return <div className="loading">Cargando...</div>

  return (
    <div className="admin-page">
      <div className="admin-header">
        <h1>Panel de administración</h1>
        <p className="admin-subtitle">Gestiona usuarios y eventos del sistema</p>
      </div>
      <section className="admin-section">
        <h2>Crear usuario</h2>
        <form onSubmit={handleCrearUsuario}>
          <input
            placeholder="Nombre"
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
          <input
            type="password"
            placeholder="Contraseña"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />
          <CustomSelect
            className="admin"
            value={form.rol}
            onChange={(rol) => setForm({ ...form, rol })}
            options={[
              { value: 'asistente', label: 'Asistente' },
              { value: 'admin', label: 'Admin' }
            ]}
          />
          <button type="submit" className="btn btn-primary">Crear usuario</button>
        </form>
        {msg && <p className={msg.includes('creado') ? 'msg-ok' : 'msg-err'}>{msg}</p>}
      </section>
      <section className="admin-section">
        <h2>Usuarios ({usuarios.length})</h2>
        <div className="usuarios-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Email</th>
                <th>Rol</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((u) => (
                <tr key={u.id}>
                  <td>{u.id}</td>
                  <td>{u.nombre}</td>
                  <td>{u.email}</td>
                  <td><span className={`rol-badge ${u.rol}`}>{u.rol}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}
