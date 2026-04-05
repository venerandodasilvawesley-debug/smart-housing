import { useEffect, useState } from 'react'
import api from '../../api/client'
import { useAuth } from '../../context/AuthContext'
import Modal from '../../components/Modal'
import Alert from '../../components/Alert'

const empty = { numero: '', capacidade: '' }

export default function QuartosPage() {
  const { user } = useAuth()
  const isAdmin = user?.role === 'admin'

  const [items, setItems] = useState([])
  const [modal, setModal] = useState(null)
  const [selected, setSelected] = useState(null)
  const [form, setForm] = useState(empty)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => { load() }, [])

  async function load() {
    const { data } = await api.get('/quartos/')
    setItems(data)
  }

  function openCreate() {
    setForm(empty)
    setError('')
    setModal('create')
  }

  function openEdit(item) {
    setSelected(item)
    setForm({ numero: item.numero, capacidade: item.capacidade, ocupacao_atual: item.ocupacao_atual })
    setError('')
    setModal('edit')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      const payload = { numero: Number(form.numero), capacidade: Number(form.capacidade) }
      if (modal === 'create') {
        await api.post('/quartos/', payload)
        setSuccess('Quarto criado.')
      } else {
        await api.put(`/quartos/${selected.id}`, payload)
        setSuccess('Quarto atualizado.')
      }
      setModal(null)
      load()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao salvar.')
    }
  }

  async function handleDelete(id) {
    if (!confirm('Remover quarto?')) return
    try {
      await api.delete(`/quartos/${id}`)
      setSuccess('Quarto removido.')
      load()
    } catch (err) {
      alert(err.response?.data?.detail || 'Erro ao remover.')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold text-gray-800">Quartos</h1>
        <button onClick={openCreate} className="bg-blue-700 hover:bg-blue-800 text-white text-sm px-4 py-2 rounded">
          + Novo
        </button>
      </div>
      <Alert type="success" message={success} />

      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
            <tr>
              <th className="px-4 py-3 text-left">ID</th>
              <th className="px-4 py-3 text-left">Número</th>
              <th className="px-4 py-3 text-left">Capacidade</th>
              <th className="px-4 py-3 text-left">Ocupação</th>
              <th className="px-4 py-3 text-left">Status</th>
              <th className="px-4 py-3 text-left">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {items.map((q) => {
              const cheio = q.ocupacao_atual >= q.capacidade
              return (
                <tr key={q.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-400">{q.id}</td>
                  <td className="px-4 py-3 font-medium">{q.numero}</td>
                  <td className="px-4 py-3">{q.capacidade}</td>
                  <td className="px-4 py-3">{q.ocupacao_atual}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${cheio ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-700'}`}>
                      {cheio ? 'Cheio' : 'Disponível'}
                    </span>
                  </td>
                  <td className="px-4 py-3 flex gap-2">
                    <button onClick={() => openEdit(q)} className="text-blue-600 hover:underline text-xs">Editar</button>
                    {isAdmin && (
                      <button onClick={() => handleDelete(q.id)} className="text-red-500 hover:underline text-xs">Remover</button>
                    )}
                  </td>
                </tr>
              )
            })}
            {items.length === 0 && (
              <tr><td colSpan={6} className="px-4 py-6 text-center text-gray-400">Nenhum quarto encontrado.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {modal && (
        <Modal title={modal === 'create' ? 'Novo Quarto' : 'Editar Quarto'} onClose={() => setModal(null)}>
          <Alert type="error" message={error} />
          <form onSubmit={handleSubmit} className="space-y-3">
            <NumField label="Número *" value={form.numero} onChange={(v) => setForm({ ...form, numero: v })} />
            <NumField label="Capacidade *" value={form.capacidade} onChange={(v) => setForm({ ...form, capacidade: v })} />
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

function NumField({ label, value, onChange }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
      <input
        type="number"
        min="1"
        className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required
      />
    </div>
  )
}
