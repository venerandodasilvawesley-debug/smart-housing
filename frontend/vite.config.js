import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/auth': 'http://localhost:8000',
      '/colaboradores': 'http://localhost:8000',
      '/quartos': 'http://localhost:8000',
      '/alocacoes': 'http://localhost:8000',
      '/manutencoes': 'http://localhost:8000',
    },
  },
})
