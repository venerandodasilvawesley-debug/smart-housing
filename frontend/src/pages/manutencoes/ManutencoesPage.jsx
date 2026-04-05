import { useEffect, useState } from 'react'
import api from '../../api/client'
import { useAuth } from '../../context/AuthContext'
import Modal from '../../components/Modal'
import Alert from '../../components/Alert'

const STATUS = ['Aberto', 'Em andamento', 'Fechado']
const STATUS_COLORS = {
  'Aberto': 'bg-red-100 text-red-600',
  'Em andamento': 'bg-yellow-100 text-yellow-700',
  'Fechado': 'bg-green-100 text-green-700',
}

const empty = { quarto_id: '', descricao: '', status: 'Aberto' }

export default function ManutencoesPage() {
  const { user } = useAuth()
  const isAdmin = user?.role === 'admin'

  const [items, setItems] = useState([])
  const [quartos, setQuartos] = useState([])
  const [modal, setModal] = useState(null)
  const [selected, setSelected] = useState(null)
  const [form, setForm] = useState(empty)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    load()
    api.get('/quartos/').then(r => setQuartos(r.data))
  }, [])

  async function load() {
    const { data } = await api.get('/manutencoes/')
    setItems(data)
  }

  function openCreate() {
    setForm(empty)
    setError('')
    setModal('create')
  }

  function openEdit(item) {
    setSelected(item)
    setForm({ descricao: item.descricao, status: item.status })
    setError('')
    setModal('edit')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      if (modal === 'create') {
        await api.post('/manutencoes/', { ...form, quarto_id: Number(form.quarto_id) })
        setSuccess('Manutenção aberta.')
      } else {
        const payload = { descricao: form.descricao, status: form.status }
        if (form.status === 'Fechado') payload.data_fechamento = new Date().toISOString()
        await api.put(`/manutencoes/${selected.id}`, payload)
        setSuccess('Manutenção atualizada.')
      }
      setModal(null)
      load()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao salvar.')
    }
  }

  async function handleDelete(id) {
    if (!confirm('Remover manutenção?')) return
    try {
      await api.delete(`/manutencoes/${id}`)
      setSuccess('Manutenção removida.')
      load()
    } catch (err) {
      alert(err.response?.data?.detail || 'Erro ao remover.')
    }
  }

  const numQuarto = (id) => quartos.find(q => q.id === id)?.numero ?? id

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold text-gray-800">Manutenções</h1>
        <button onClick={openCreate} className="bg-blue-700 hover:bg-blue-800 text-white text-sm px-4 py-2 rounded">
          + Nova
        </button>
      </div>
      <Alert type="success" message={success} />

      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
            <tr>
              <th className="px-4 py-3 text-left">ID</th>
              <th className="px-4 py-3 text-left">Quarto</th>
              <th className="px-4 py-3 text-left">Descrição</th>
              <th className="px-4 py-3 text-left">Status</th>
              <th className="px-4 py-3 text-left">Abertura</th>
              <th className="px-4 py-3 text-left">Fechamento</th>
              <th className="px-4 py-3 text-left">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {items.map((m) => (
              <tr key={m.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-gray-400">{m.id}</td>
                <td className="px-4 py-3">{numQuarto(m.quarto_id)}</td>
                <td className="px-4 py-3 max-w-xs truncate">{m.descricao}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_COLORS[m.status]}`}>
                    {m.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-xs">{m.data_abertura ? new Date(m.data_abertura).toLocaleString('pt-BR') : '—'}</td>
                <td className="px-4 py-3 text-xs">{m.data_fechamento ? new Date(m.data_fechamento).toLocaleString('pt-BR') : '—'}</td>
                <td className="px-4 py-3 flex gap-2">
                  <button onClick={() => openEdit(m)} className="text-blue-600 hover:underline text-xs">Editar</button>
                  {isAdmin && (
                    <button onClick={() => handleDelete(m.id)} className="text-red-500 hover:underline text-xs">Remover</button>
                  )}
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr><td colSpan={7} className="px-4 py-6 text-center text-gray-400">Nenhuma manutenção encontrada.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {modal && (
        <Modal title={modal === 'create' ? 'Nova Manutenção' : 'Editar Manutenção'} onClose={() => setModal(null)}>
          <Alert type="error" message={error} />
          <form onSubmit={handleSubmit} className="space-y-3">
            {modal === 'create' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Quarto *</label>
                <select
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                  value={form.quarto_id}
                  onChange={(e) => setForm({ ...form, quarto_id: e.target.value })}
                  required
                >
                  <option value="">Selecione...</option>
                  {quartos.map(q => (
                    <option key={q.id} value={q.id}>Quarto {q.numero}</option>
                  ))}
                </select>
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Descrição *</label>
              <textarea
                className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                rows={3}
                minLength={5}
                value={form.descricao}
                onChange={(e) => setForm({ ...form, descricao: e.target.value })}
                required
              />
            </div>
            {modal === 'edit' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                  value={form.status}
                  onChange={(e) => setForm({ ...form, status: e.target.value })}
                >
                  {STATUS.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
            )}
            <div className="flex justify-end gap-2 pt-2">
              <button type="button" onClick={() => setModal(null)} className="text-sm px-4 py-2 border rounded hover:bg-gray-50">Cancelar</button>
              <button type="submit" className="text-sm px-4 py-2 bg-blue-700 text-white rounded hover:bg-blue-800">Salvar</button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  )
}
