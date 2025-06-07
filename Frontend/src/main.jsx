import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import Landingpage from './Landingpage.jsx'
import Chatbotpage from './Chatbotpage.jsx'

createRoot(document.getElementById('root')).render(
 <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landingpage />} />
        <Route path="/chatbot" element={<Chatbotpage />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
