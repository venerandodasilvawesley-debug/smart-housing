export default function Alert({ type = 'error', message }) {
  if (!message) return null
  const styles = {
    error: 'bg-red-50 border-red-400 text-red-700',
    success: 'bg-green-50 border-green-400 text-green-700',
  }
  return (
    <div className={`border rounded px-4 py-3 text-sm my-3 ${styles[type]}`}>
      {message}
    </div>
  )
}
