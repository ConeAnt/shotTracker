import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'build',  // You can specify the output directory here if you want 'build' instead of 'dist'
  },
  base: '/shotTracker/',
  plugins: [react()]
})
