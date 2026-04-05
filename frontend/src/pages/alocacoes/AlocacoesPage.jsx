import { useEffect, useState } from 'react'
import api from '../../api/client'
import { useAuth } from '../../context/AuthContext'
import Modal from '../../components/Modal'
import Alert from '../../components/Alert'

const today = () => new Date().toISOString().split('T')[0]
const empty = { colaborador_id: '', quarto_id: '', data_entrada: today(), data_saida: '' }

export default function AlocacoesPage() {
  const { user } = useAuth()
  const isAdmin = user?.role === 'admin'

  const [items, setItems] = useState([])
  const [colaboradores, setColaboradores] = useState([])
  const [quartos, setQuartos] = useState([])
  const [modal, setModal] = useState(null)
  const [selected, setSelected] = useState(null)
  const [form, setForm] = useState(empty)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    load()
    api.get('/colaboradores/').then(r => setColaboradores(r.data))
    api.get('/quartos/').then(r => setQuartos(r.data))
  }, [])

  async function load() {
    const { data } = await api.get('/alocacoes/')
    setItems(data)
  }

  function openCreate() {
    setForm(empty)
    setError('')
    setModal('create')
  }

  function openEdit(item) {
    setSelected(item)
    setForm({ data_saida: item.data_saida ?? '' })
    setError('')
    setModal('edit')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      if (modal === 'create') {
        const payload = {
          colaborador_id: Number(form.colaborador_id),
          quarto_id: Number(form.quarto_id),
          data_entrada: form.data_entrada,
          ...(form.data_saida ? { data_saida: form.data_saida } : {}),
        }
        await api.post('/alocacoes/', payload)
        setSuccess('Alocação criada.')
      } else {
        await api.put(`/alocacoes/${selected.id}`, { data_saida: form.data_saida || null })
        setSuccess('Alocação atualizada.')
      }
      setModal(null)
      load()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao salvar.')
    }
  }

  async function handleDelete(id) {
    if (!confirm('Desalocar colaborador?')) return
    try {
      await api.delete(`/alocacoes/${id}`)
      setSuccess('Colaborador desalocado.')
      load()
    } catch (err) {
      alert(err.response?.data?.detail || 'Erro ao desalocar.')
    }
  }

  const nomeColaborador = (id) => colaboradores.find(c => c.id === id)?.nome ?? id
  const numQuarto = (id) => quartos.find(q => q.id === id)?.numero ?? id

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold text-gray-800">Alocações</h1>
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
              <th className="px-4 py-3 text-left">Colaborador</th>
              <th className="px-4 py-3 text-left">Quarto</th>
              <th className="px-4 py-3 text-left">Entrada</th>
              <th className="px-4 py-3 text-left">Saída</th>
              <th className="px-4 py-3 text-left">Status</th>
              <th className="px-4 py-3 text-left">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {items.map((a) => (
              <tr key={a.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-gray-400">{a.id}</td>
                <td className="px-4 py-3">{nomeColaborador(a.colaborador_id)}</td>
                <td className="px-4 py-3">{numQuarto(a.quarto_id)}</td>
                <td className="px-4 py-3">{a.data_entrada}</td>
                <td className="px-4 py-3">{a.data_saida ?? '—'}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${!a.data_saida ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                    {!a.data_saida ? 'Ativa' : 'Encerrada'}
                  </span>
                </td>
                <td className="px-4 py-3 flex gap-2">
                  <button onClick={() => openEdit(a)} className="text-blue-600 hover:underline text-xs">Editar</button>
                  {isAdmin && (
                    <button onClick={() => handleDelete(a.id)} className="text-red-500 hover:underline text-xs">Desalocar</button>
                  )}
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr><td colSpan={7} className="px-4 py-6 text-center text-gray-400">Nenhuma alocação encontrada.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {modal && (
        <Modal title={modal === 'create' ? 'Nova Alocação' : 'Editar Saída'} onClose={() => setModal(null)}>
          <Alert type="error" message={error} />
          <form onSubmit={handleSubmit} className="space-y-3">
            {modal === 'create' && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Colaborador *</label>
                  <select
                    className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                    value={form.colaborador_id}
                    onChange={(e) => setForm({ ...form, colaborador_id: e.target.value })}
                    required
                  >
                    <option value="">Selecione...</option>
                    {colaboradores.filter(c => c.ativo).map(c => (
                      <option key={c.id} value={c.id}>{c.nome} — {c.documento}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Quarto *</label>
                  <select
                    className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                    value={form.quarto_id}
                    onChange={(e) => setForm({ ...form, quarto_id: e.target.value })}
                    required
                  >
                    <option value="">Selecione...</option>
                    {quartos.filter(q => q.ocupacao_atual < q.capacidade).map(q => (
                      <option key={q.id} value={q.id}>Quarto {q.numero} ({q.ocupacao_atual}/{q.capacidade})</option>
                    ))}
                  </select>
                </div>
                <DateField label="Data de Entrada *" value={form.data_entrada} onChange={(v) => setForm({ ...form, data_entrada: v })} required />
              </>
            )}
            <DateField label="Data de Saída" value={form.data_saida} onChange={(v) => setForm({ ...form, data_saida: v })} />
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

function DateField({ label, value, onChange, required }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
      <input
        type="date"
        className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
      />
    </div>
  )
}
