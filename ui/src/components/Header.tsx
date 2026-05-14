import { useFactoryStore } from '../store/factory.store'
import { Wifi, WifiOff, Play, Square } from 'lucide-react'

export default function Header() {
  const { connected } = useFactoryStore()
  
  return (
    <header className="h-14 bg-[#111] border-b border-[#1e1e1e] flex items-center justify-between px-4">
      <div className="flex items-center gap-4">
        <h1 className="text-lg font-semibold">AI Software Factory</h1>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-sm">
          {connected ? (
            <><Wifi className="w-4 h-4 text-green-500" /><span className="text-green-500">Connected</span></>
          ) : (
            <><WifiOff className="w-4 h-4 text-red-500" /><span className="text-red-500">Disconnected</span></>
          )}
        </div>
        
        <button className="flex items-center gap-2 px-3 py-1.5 bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors">
          <Play className="w-4 h-4" /> Run
        </button>
      </div>
    </header>
  )
}