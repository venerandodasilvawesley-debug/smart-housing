import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/colaboradores', label: 'Colaboradores' },
  { to: '/quartos', label: 'Quartos' },
  { to: '/alocacoes', label: 'Alocações' },
  { to: '/manutencoes', label: 'Manutenções' },
]

export default function Layout({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <nav className="bg-blue-700 text-white shadow">
        <div className="max-w-6xl mx-auto px-4 flex items-center justify-between h-14">
          <span className="font-bold text-lg tracking-tight">🏠 Smart Housing</span>
          <div className="flex gap-4 items-center">
            {links.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `text-sm font-medium px-2 py-1 rounded transition ${
                    isActive ? 'bg-blue-900' : 'hover:bg-blue-600'
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
            <span className="text-xs text-blue-200 ml-2">{user?.username} ({user?.role})</span>
            <button
              onClick={handleLogout}
              className="text-sm bg-blue-900 hover:bg-blue-800 px-3 py-1 rounded"
            >
              Sair
            </button>
          </div>
        </div>
      </nav>
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 py-6">{children}</main>
    </div>
  )
}
