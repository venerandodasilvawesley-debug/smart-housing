import { useEffect, useState } from 'react'
import api from '../../api/client'
import { useAuth } from '../../context/AuthContext'
import Modal from '../../components/Modal'
import Alert from '../../components/Alert'

const empty = { nome: '', documento: '', empresa: '', setor: '', ativo: true }

export default function ColaboradoresPage() {
  const { user } = useAuth()
  const isAdmin = user?.role === 'admin'

  const [items, setItems] = useState([])
  const [modal, setModal] = useState(null) // null | 'create' | 'edit'
  const [selected, setSelected] = useState(null)
  const [form, setForm] = useState(empty)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => { load() }, [])

  async function load() {
    const { data } = await api.get('/colaboradores/')
    setItems(data)
  }

  function openCreate() {
    setForm(empty)
    setError('')
    setModal('create')
  }

  function openEdit(item) {
    setSelected(item)
    setForm({ nome: item.nome, empresa: item.empresa ?? '', setor: item.setor ?? '', ativo: item.ativo })
    setError('')
    setModal('edit')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      if (modal === 'create') {
        await api.post('/colaboradores/', form)
        setSuccess('Colaborador criado com sucesso.')
      } else {
        await api.put(`/colaboradores/${selected.id}`, form)
        setSuccess('Colaborador atualizado.')
      }
      setModal(null)
      load()
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao salvar.')
    }
  }

  async function handleDelete(id) {
    if (!confirm('Remover colaborador?')) return
    try {
      await api.delete(`/colaboradores/${id}`)
      setSuccess('Colaborador removido.')
      load()
    } catch (err) {
      setSuccess('')
      alert(err.response?.data?.detail || 'Erro ao remover.')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold text-gray-800">Colaboradores</h1>
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
              <th className="px-4 py-3 text-left">Nome</th>
              <th className="px-4 py-3 text-left">Documento</th>
              <th className="px-4 py-3 text-left">Empresa</th>
              <th className="px-4 py-3 text-left">Setor</th>
              <th className="px-4 py-3 text-left">Ativo</th>
              <th className="px-4 py-3 text-left">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {items.map((c) => (
              <tr key={c.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-gray-400">{c.id}</td>
                <td className="px-4 py-3 font-medium">{c.nome}</td>
                <td className="px-4 py-3">{c.documento}</td>
                <td className="px-4 py-3">{c.empresa ?? '—'}</td>
                <td className="px-4 py-3">{c.setor ?? '—'}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${c.ativo ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'}`}>
                    {c.ativo ? 'Sim' : 'Não'}
                  </span>
                </td>
                <td className="px-4 py-3 flex gap-2">
                  <button onClick={() => openEdit(c)} className="text-blue-600 hover:underline text-xs">Editar</button>
                  {isAdmin && (
                    <button onClick={() => handleDelete(c.id)} className="text-red-500 hover:underline text-xs">Remover</button>
                  )}
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr><td colSpan={7} className="px-4 py-6 text-center text-gray-400">Nenhum colaborador encontrado.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {modal && (
        <Modal title={modal === 'create' ? 'Novo Colaborador' : 'Editar Colaborador'} onClose={() => setModal(null)}>
          <Alert type="error" message={error} />
          <form onSubmit={handleSubmit} className="space-y-3">
            <Field label="Nome *" value={form.nome} onChange={(v) => setForm({ ...form, nome: v })} required />
            {modal === 'create' && (
              <Field label="Documento *" value={form.documento} onChange={(v) => setForm({ ...form, documento: v })} required />
            )}
            <Field label="Empresa" value={form.empresa} onChange={(v) => setForm({ ...form, empresa: v })} />
            <Field label="Setor" value={form.setor} onChange={(v) => setForm({ ...form, setor: v })} />
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={form.ativo} onChange={(e) => setForm({ ...form, ativo: e.target.checked })} />
              Ativo
            </label>
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

function Field({ label, value, onChange, required }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
      <input
        className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
      />
    </div>
  )
}
