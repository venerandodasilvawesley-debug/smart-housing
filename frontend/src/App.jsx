import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import PrivateRoute from './components/PrivateRoute'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import ColaboradoresPage from './pages/colaboradores/ColaboradoresPage'
import QuartosPage from './pages/quartos/QuartosPage'
import AlocacoesPage from './pages/alocacoes/AlocacoesPage'
import ManutencoesPage from './pages/manutencoes/ManutencoesPage'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/*"
            element={
              <PrivateRoute>
                <Layout>
                  <Routes>
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/colaboradores" element={<ColaboradoresPage />} />
                    <Route path="/quartos" element={<QuartosPage />} />
                    <Route path="/alocacoes" element={<AlocacoesPage />} />
                    <Route path="/manutencoes" element={<ManutencoesPage />} />
                  </Routes>
                </Layout>
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
