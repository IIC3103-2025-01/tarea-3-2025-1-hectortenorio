import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function Landingpage() {
  const [message, setMessage] = useState('')
  const navigate = useNavigate()

  const handleSend = async () => {
      try {
        const response = await axios.post('https://tarea-3-2025-1-hectortenorio.onrender.com/scrape', {
          url: message
        })
        console.log('✅ Respuesta del backend:', response.data)
        alert('Scraping realizado con éxito.')
        setMessage('')
        navigate('/chatbot')

      } catch (error) {
        console.error('❌ Error al hacer scraping:', error.response?.data || error.message)
        alert('El link ingresado no es válido. Intente con otro nuevamente.')
        setMessage('')
      }
    }


  return (
    <div className="flex flex-col items-center justify-center min-h-screen overflow-hidden">
      <div className="absolute top-[1rem] left-[1.5rem] text-[1.5rem]  font-bold text-[#000000']">
        WikiBot
      </div>
      <div className="relative w-[50rem]">
        <input 
          type="text " 
          placeholder="Bienvenido, Ingrese un link de Wikipedia valido" 
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="w-full h-[4rem] pl-[0.4rem] rounded-lg focus:outline-none text-[1.05rem]  focus:ring-[#F5F8FB] "
        />
        <button 
          onClick={handleSend}
          className="absolute bottom-[0.2rem] left-[47.2rem] bg-[#0176DE] hover:bg-[#173F8A] text-[#FFFFFF]  rounded-md"
        >
          Enviar
        </button>
      </div>
    </div>
  )
}

export default Landingpage


//'light-blue': '#0176DE',
  //      'blue': '#173F8A',
    //    'dark-blue': '#03122E',
      //  'sky-blue': '#16D4EE',
      //  'yellow': '#FEC60D',
       // 'yellow-bright': '#FFFF00',
       // 'red': '#F24F4F',
      //  'dark-red': '#921818',
       // 'green': '#00AA00',
       // 'white': '#FFFFFF',
       // 'black': '#000000',
       // 'purple': '#BD32EE',
       // 'orange': '#FF7A00',
       // 'grey': '#E3E8E8',
       // 'light-grey': '#F5F8FB',
        //'dark-grey': '#9C9C9C',
       // 'hyper-light-grey': '#F6F6F6'