import { NavLink } from 'react-router-dom'
import { Factory, Code, Bot, Terminal, FolderOpen, Settings } from 'lucide-react'

interface Props {
  open: boolean
  onToggle: () => void
}

export default function Sidebar({ open }: Props) {
  return (
    <aside className={`${open ? 'w-60' : 'w-16'} bg-[#111] border-r border-[#1e1e1e] flex flex-col transition-all`}>
      <div className="p-4 border-b border-[#1e1e1e]">
        <div className="flex items-center gap-3">
          <Factory className="w-8 h-8 text-indigo-500" />
          {open && <span className="font-bold text-lg">Factory</span>}
        </div>
      </div>
      
      <nav className="flex-1 p-2 space-y-1">
        <NavLink to="/" className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#1e1e1e] transition-colors">
          <Factory className="w-5 h-5" />
          {open && <span>Dashboard</span>}
        </NavLink>
        
        <NavLink to="/projects" className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#1e1e1e] transition-colors">
          <FolderOpen className="w-5 h-5" />
          {open && <span>Projects</span>}
        </NavLink>
        
        <NavLink to="/agents" className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#1e1e1e] transition-colors">
          <Bot className="w-5 h-5" />
          {open && <span>Agents</span>}
        </NavLink>
        
        <NavLink to="/terminal" className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#1e1e1e] transition-colors">
          <Terminal className="w-5 h-5" />
          {open && <span>Terminal</span>}
        </NavLink>
      </nav>
      
      <div className="p-2 border-t border-[#1e1e1e]">
        <button className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#1e1e1e] transition-colors w-full">
          <Settings className="w-5 h-5" />
          {open && <span>Settings</span>}
        </button>
      </div>
    </aside>
  )
}