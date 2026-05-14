import { useFactoryStore } from '../store/factory.store'
import { Link } from 'react-router-dom'
import { Plus, FolderOpen, Bot, Play, Activity } from 'lucide-react'

export default function Dashboard() {
  const { agents, projects, connected } = useFactoryStore()
  
  return (
    <div className="space-y-6">
      {/* Welcome */}
      <div className="panel p-6">
        <h2 className="text-2xl font-bold mb-2">Welcome to AI Software Factory</h2>
        <p className="text-zinc-400 mb-4">Build production-ready apps with AI agents</p>
        
        <div className="flex gap-3">
          <Link to="/project/new" className="btn-primary flex items-center gap-2">
            <Plus className="w-4 h-4" /> New Project
          </Link>
        </div>
      </div>
      
      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link to="/projects" className="panel p-4 hover:border-indigo-500 transition-colors cursor-pointer">
          <div className="flex items-center gap-3">
            <FolderOpen className="w-8 h-8 text-indigo-500" />
            <div>
              <h3 className="font-semibold">Projects</h3>
              <p className="text-sm text-zinc-400">{projects.length} projects</p>
            </div>
          </div>
        </Link>
        
        <Link to="/agents" className="panel p-4 hover:border-indigo-500 transition-colors cursor-pointer">
          <div className="flex items-center gap-3">
            <Bot className="w-8 h-8 text-green-500" />
            <div>
              <h3 className="font-semibold">AI Agents</h3>
              <p className="text-sm text-zinc-400">{agents.length} agents ready</p>
            </div>
          </div>
        </Link>
      </div>
      
      {/* Agents Status */}
      <div className="panel p-4">
        <h3 className="font-semibold mb-4">Agent Status</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {agents.map((agent) => (
            <div key={agent.type} className="p-3 bg-[#0a0a0a] rounded-lg">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xl">{agent.emoji}</span>
                <span className="font-medium">{agent.name}</span>
              </div>
              <div className="text-xs text-zinc-500">{agent.role}</div>
              <div className={`text-xs mt-1 ${agent.status === 'working' ? 'text-green-500' : 'text-zinc-500'}`}>
                ● {agent.status}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}