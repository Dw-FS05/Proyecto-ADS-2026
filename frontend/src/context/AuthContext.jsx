import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        setUser({ id: payload.user_id, rol: payload.rol })
      } catch {}
    }
  }, [])

  const login = (token, rol) => {
    localStorage.setItem('token', token)
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      setUser({ id: payload.user_id, rol: rol || payload.rol })
    } catch {}
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
