import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx'

try {
  const rootElement = document.getElementById('root')
  if (!rootElement) {
    throw new Error('Root element not found')
  }

  const root = createRoot(rootElement)
  root.render(
    <BrowserRouter>
      <App />
    </BrowserRouter>,
  )
} catch (error) {
  console.error('Error rendering application:', error)
}