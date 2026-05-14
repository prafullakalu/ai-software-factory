import { useEffect, useRef, useState } from 'react'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import 'xterm/css/xterm.css'

const WS_URL = 'ws://localhost:8000/ws/terminal'

export default function Terminal_() {
  const containerRef = useRef<HTMLDivElement>(null)
  const termRef = useRef<Terminal | null>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const [connected, setConnected] = useState(false)
  
  useEffect(() => {
    if (!containerRef.current) return
    
    // Initialize xterm
    const term = new Terminal({
      theme: {
        background: '#0a0a0a',
        foreground: '#f4f4f5',
        cursor: '#6366f1',
        cursorAccent: '#0a0a0a',
        selectionBackground: '#6366f140',
        black: '#1e1e1e',
        green: '#22c55e',
        yellow: '#f59e0b',
        blue: '#3b82f6',
        cyan: '#06b6d4',
        red: '#ef4444',
      },
      fontFamily: 'JetBrains Mono, Fira Code, monospace',
      fontSize: 13,
      lineHeight: 1.5,
      cursorBlink: true,
      cursorStyle: 'bar',
    })
    
    const fitAddon = new FitAddon()
    term.loadAddon(fitAddon)
    term.open(containerRef.current)
    fitAddon.fit()
    
    termRef.current = term
    
    // Connect WebSocket
    const ws = new WebSocket(WS_URL)
    wsRef.current = ws
    
    ws.onopen = () => {
      setConnected(true)
      term.writeln('\x1b[1;32m🏭 AI Software Factory Terminal\x1b[0m')
      term.writeln('\x1b[2mConnected to factory server\x1b[0m')
      term.write('\x1b[1;36m$ \x1b[0m')
    }
    
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data)
      if (data.type === 'output') {
        term.write(data.text)
      }
    }
    
    ws.onclose = () => {
      setConnected(false)
      term.writeln('\x1b[1;31m\r\nDisconnected from server\x1b[0m')
    }
    
    // Input handling
    let buffer = ''
    term.onData((data) => {
      if (data === '\r') {
        ws.send(JSON.stringify({ type: 'input', command: buffer }))
        term.write('\r\n')
        buffer = ''
      } else if (data === '\x7f') {
        if (buffer.length > 0) {
          buffer = buffer.slice(0, -1)
          term.write('\b \b')
        }
      } else {
        buffer += data
        term.write(data)
      }
    })
    
    // Resize handler
    const observer = new ResizeObserver(() => fitAddon.fit())
    observer.observe(containerRef.current)
    
    return () => {
      term.dispose()
      ws.close()
      observer.disconnect()
    }
  }, [])
  
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-2 bg-[#111] border-b border-[#1e1e1e]">
        <span className="text-sm font-medium">Terminal</span>
        <span className={`text-xs ${connected ? 'text-green-500' : 'text-red-500'}`}>
          {connected ? '● Connected' : '○ Disconnected'}
        </span>
      </div>
      <div ref={containerRef} className="flex-1 p-2" />
    </div>
  )
}