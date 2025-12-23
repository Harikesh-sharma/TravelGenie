import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/plan': 'http://127.0.0.1:8000',
      '/subscribe': 'http://127.0.0.1:8000',
    },
  },
})