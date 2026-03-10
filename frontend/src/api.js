import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const login = (email, password) => api.post('/login', { email, password })
export const getEventos = () => api.get('/eventos')
export const getEvento = (id) => api.get(`/eventos/${id}`)
export const crearEvento = (data) => api.post('/eventos', data)
export const registrarAsistente = (eventoId, usuarioId) =>
  api.post(`/eventos/${eventoId}/registrar`, { usuario_id: usuarioId })
export const getUsuarios = () => api.get('/admin/usuarios')
export const crearUsuario = (data) => api.post('/admin/usuarios', data)
