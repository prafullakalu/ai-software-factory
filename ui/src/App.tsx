import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { FactoryStore, useFactoryStore } from './store/factory.store'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import ProjectView from './pages/ProjectView'
import AgentChat from './pages/AgentChat'
import Terminal from './components/Terminal'

// WebSocket hook
function useWebSocket() {
  const { setConnected, setAgents, addMessage, setProjects } = useFactoryStore()
  
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/factory-ui')
    
    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)
    
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data)
      
      switch (data.type) {
        case 'agent_token':
          addMessage(data.agent, data.token)
          break
        case 'agent_status':
          setAgents(data.agents)
          break
        case 'project_list':
          setProjects(data.projects)
          break
      }
    }
    
    return () => ws.close()
  }, [])
}

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-[#0a0a0a] text-zinc-100">
        <Sidebar open={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header />
          
          <main className="flex-1 overflow-auto p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/project/:name" element={<ProjectView />} />
              <Route path="/agent/:type" element={<AgentChat />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}