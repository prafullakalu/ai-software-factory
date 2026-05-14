import { create } from 'zustand'

interface Agent {
  type: string
  name: string
  role: string
  emoji: string
  status: string
}

interface Project {
  name: string
  path: string
  files: number
}

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface FactoryState {
  connected: boolean
  currentProject: string | null
  currentAgent: string | null
  agents: Agent[]
  projects: Project[]
  messages: Record<string, Message[]>
  
  setConnected: (v: boolean) => void
  setCurrentProject: (name: string | null) => void
  setCurrentAgent: (type: string | null) => void
  setAgents: (agents: Agent[]) => void
  setProjects: (projects: Project[]) => void
  addMessage: (agent: string, content: string) => void
  clearMessages: (agent: string) => void
}

export const useFactoryStore = create<FactoryState>((set) => ({
  connected: false,
  currentProject: null,
  currentAgent: null,
  agents: [
    { type: 'cto', name: 'Atlas', role: 'CTO', emoji: '🧠', status: 'idle' },
    { type: 'developer', name: 'Forge', role: 'Developer', emoji: '💻', status: 'idle' },
    { type: 'qa', name: 'Cipher', role: 'QA', emoji: '🔍', status: 'idle' },
    { type: 'devops', name: 'Helm', role: 'DevOps', emoji: '🚀', status: 'idle' },
  ],
  projects: [],
  messages: {},
  
  setConnected: (v) => set({ connected: v }),
  setCurrentProject: (name) => set({ currentProject: name }),
  setCurrentAgent: (type) => set({ currentAgent: type }),
  setAgents: (agents) => set({ agents }),
  setProjects: (projects) => set({ projects }),
  
  addMessage: (agent, content) => set((state) => ({
    messages: {
      ...state.messages,
      [agent]: [
        ...(state.messages[agent] || []),
        {
          id: Date.now().toString(),
          role: 'assistant',
          content,
          timestamp: new Date(),
        },
      ],
    },
  })),
  
  clearMessages: (agent) => set((state) => {
    const msgs = { ...state.messages }
    delete msgs[agent]
    return { messages: msgs }
  }),
}))