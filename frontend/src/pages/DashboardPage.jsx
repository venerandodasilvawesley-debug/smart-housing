import { useEffect, useState } from 'react'
import api from '../api/client'

function StatCard({ label, value, sub, color }) {
  const colors = {
    blue: 'border-blue-500 bg-blue-50 text-blue-700',
    green: 'border-green-500 bg-green-50 text-green-700',
    yellow: 'border-yellow-500 bg-yellow-50 text-yellow-700',
    red: 'border-red-500 bg-red-50 text-red-700',
  }
  return (
    <div className={`border-l-4 rounded-lg p-5 shadow-sm bg-white ${colors[color]}`}>
      <p className="text-sm font-medium text-gray-500">{label}</p>
      <p className={`text-4xl font-bold mt-1 ${colors[color].split(' ')[2]}`}>{value ?? '—'}</p>
      {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
    </div>
  )
}

export default function DashboardPage() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    async function load() {
      const [quartos, alocacoes, manutencoes, colaboradores] = await Promise.all([
        api.get('/quartos/'),
        api.get('/alocacoes/'),
        api.get('/manutencoes/'),
        api.get('/colaboradores/'),
      ])

      const q = quartos.data
      const a = alocacoes.data
      const m = manutencoes.data
      const c = colaboradores.data

      setStats({
        totalQuartos: q.length,
        quartosDisponiveis: q.filter(x => x.ocupacao_atual < x.capacidade).length,
        alocacoesAtivas: a.filter(x => !x.data_saida).length,
        manutencoesAbertas: m.filter(x => x.status !== 'Fechado').length,
        colaboradoresAtivos: c.filter(x => x.ativo).length,
        vagasTotal: q.reduce((s, x) => s + x.capacidade, 0),
        vagasOcupadas: q.reduce((s, x) => s + x.ocupacao_atual, 0),
      })
    }
    load()
  }, [])

  const ocupacaoPct = stats
    ? stats.vagasTotal > 0
      ? Math.round((stats.vagasOcupadas / stats.vagasTotal) * 100)
      : 0
    : null

  return (
    <div>
      <h1 className="text-xl font-bold text-gray-800 mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          label="Quartos Disponíveis"
          value={stats ? `${stats.quartosDisponiveis}/${stats.totalQuartos}` : null}
          sub="com vagas abertas"
          color="green"
        />
        <StatCard
          label="Alocações Ativas"
          value={stats?.alocacoesAtivas}
          sub="colaboradores alocados"
          color="blue"
        />
        <StatCard
          label="Manutenções Abertas"
          value={stats?.manutencoesAbertas}
          sub="Aberto ou Em andamento"
          color="yellow"
        />
        <StatCard
          label="Colaboradores Ativos"
          value={stats?.colaboradoresAtivos}
          sub="cadastrados e ativos"
          color="blue"
        />
      </div>

      {stats && (
        <div className="bg-white rounded-lg shadow-sm p-5 max-w-md">
          <p className="text-sm font-medium text-gray-600 mb-2">
            Ocupação geral — {stats.vagasOcupadas} de {stats.vagasTotal} vagas
          </p>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className={`h-4 rounded-full transition-all ${
                ocupacaoPct >= 90 ? 'bg-red-500' :
                ocupacaoPct >= 60 ? 'bg-yellow-400' : 'bg-green-500'
              }`}
              style={{ width: `${ocupacaoPct}%` }}
            />
          </div>
          <p className="text-xs text-gray-400 mt-1">{ocupacaoPct}% ocupado</p>
        </div>
      )}
    </div>
  )
}
