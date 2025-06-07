import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'


function Chatbotpage(){
    const navigate = useNavigate()
    const [message, setMessage] = useState('')
    const [isSending, setIsSending] = useState(false)
    const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hola, ¿en qué puedo ayudarte hoy?' }
    ])

   const handleSend = async () => {
        if (!message.trim()) return
        setIsSending(true) // desactiv
        const userMessage = { type: 'user', text: message }
        setMessages(prev => [...prev, userMessage])
        setMessage('')
        console.log("userMessage:", userMessage)


        try {
          const response = await axios.post('https://tarea-3-2025-1-hectortenorio.onrender.com/talk', {
            pregunta: message,
          })
          console.log(userMessage)
          const botReply = {
            type: 'bot',
            text: response.data.respuesta || 'Lo siento, no pude procesar tu pregunta.',
          }

          setMessages(prev => [...prev, botReply])
        } catch (error) {
          const botError = {
            type: 'bot',
            text: '❌ Error al conectar con el modelo.',
          }
          setMessages(prev => [...prev, botError])
          console.error(error)
        }
      setTimeout(() => setIsSending(false), 1000)
    }


    const handleBack  = async () => {
        const confirmed = confirm (
            'Si vuelves, deberás ingresar un nuevo enlace y se perderá el historial del chat actual.\n\n¿Estás seguro de que deseas continuar?'
        )
        if (confirmed) {
            navigate('/')
        }
    }
  return (
    <div className="flex flex-col h-screen">
      <div className="flex justify-between items-center">
        <div className="text-[1.5rem] font-bold text-[#000000']">WikiBot</div>
        <h1 className="text-3xl text-center font-semibold mt-12">¡Bienvenido al Chat!</h1>
        <button
          onClick={handleBack}
          className="bg-[#F24F4F] hover:bg-[#921818] text-[#FFFFFF] py-[0.5rem] px-[1rem] rounded-lg"
        >
          Volver
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4 bg-white">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-[70%] px-[1.2rem] py-[0.3rem] rounded-lg break-words ${
              msg.type === 'user'
                ? 'ml-auto text-right'
                : 'mr-auto text-left'
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>
 
      <div className="relative py-[1.2rem] ">
        <div className="relative w-[50rem] mx-auto pr-[0.4rem] ">
          <input
            type="text"
            placeholder="Escribe un mensaje..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className=" pl-[0.2rem] w-full h-[3rem] pr-28 rounded-lg border text-[1rem] "
          />
          <button
            onClick={handleSend}  // En el enunciado se menciona que no se puedan hacer mas de 10 request por segundo con esto se limita y se asegura
            disabled={isSending}  // que no se puede enviar mas de 1 request por segundo     
            className={`absolute right-[0rem] px-[1rem] rounded-md text-white h-[3rem] ${
              isSending
                ? 'bg-[#E3E8E8] cursor-not-allowed'
                : 'bg-[#0176DE] hover:bg-[#173F8A]'
            }`}
          >
            {isSending ? 'Enviando...' : 'Enviar'}
          </button>
        </div>
      </div>
    </div>
  )
}



export default Chatbotpage






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