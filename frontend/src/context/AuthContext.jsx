import { createContext, useContext, useState, useEffect } from 'react'
import api from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const stored = localStorage.getItem('user')
    if (token && stored) setUser(JSON.parse(stored))
    setLoading(false)
  }, [])

  async function login(username, password) {
    const form = new URLSearchParams({ username, password })
    const { data } = await api.post('/auth/token', form)
    localStorage.setItem('token', data.access_token)
    // decode payload to get role
    const payload = JSON.parse(atob(data.access_token.split('.')[1]))
    const userData = { username: payload.sub, role: payload.role }
    localStorage.setItem('user', JSON.stringify(userData))
    setUser(userData)
    return userData
  }

  function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
