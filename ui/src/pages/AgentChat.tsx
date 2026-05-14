import { useParams, Link } from 'react-router-dom'
import { useFactoryStore } from '../store/factory.store'
import { useState } from 'react'

export default function AgentChat() {
  const { type } = useParams()
  const { agents, messages, addMessage } = useFactoryStore()
  const [input, setInput] = useState('')
  
  const agent = agents.find((a) => a.type === type)
  const agentMessages = messages[type || ''] || []
  
  const sendMessage = () => {
    if (!input.trim()) return
    addMessage(type || '', input)
    setInput('')
    
    // Would send to WebSocket
    fetch(`/api/agents/${type}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agent: type, message: input }),
    })
  }
  
  if (!agent) {
    return (
      <div className="panel p-6 text-center">
        <h2 className="text-xl font-semibold mb-2">Agent Not Found</h2>
        <Link to="/agents" className="text-indigo-500 hover:underline">Back to Agents</Link>
      </div>
    )
  }
  
  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="panel p-4 flex items-center gap-3">
        <span className="text-3xl">{agent.emoji}</span>
        <div>
          <h2 className="text-xl font-semibold">{agent.name}</h2>
          <p className="text-sm text-zinc-400">{agent.role}</p>
        </div>
      </div>
      
      {/* Messages */}
      <div className="flex-1 panel p-4 overflow-auto space-y-4">
        {agentMessages.length === 0 ? (
          <div className="text-center text-zinc-500 py-8">
            Start a conversation with {agent.name}
          </div>
        ) : (
          agentMessages.map((msg) => (
            <div key={msg.id} className={`p-3 rounded-lg ${msg.role === 'user' ? 'bg-indigo-900/30 ml-8' : 'mr-8'}`}>
              {msg.content}
            </div>
          ))
        )}
      </div>
      
      {/* Input */}
      <div className="panel p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder={`Message ${agent.name}...`}
            className="input"
          />
          <button onClick={sendMessage} className="btn-primary">Send</button>
        </div>
      </div>
    </div>
  )
}