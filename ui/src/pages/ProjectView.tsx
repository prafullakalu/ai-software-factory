import { useParams, Link } from 'react-router-dom'
import { useFactoryStore } from '../store/factory.store'

export default function ProjectView() {
  const { name } = useParams()
  const { projects } = useFactoryStore()
  const project = projects.find((p) => p.name === name)
  
  if (!project) {
    return (
      <div className="panel p-6 text-center">
        <h2 className="text-xl font-semibold mb-2">Project Not Found</h2>
        <Link to="/projects" className="text-indigo-500 hover:underline">Back to Projects</Link>
      </div>
    )
  }
  
  return (
    <div className="space-y-4">
      <div className="panel p-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">{project.name}</h2>
          <p className="text-sm text-zinc-400">{project.files} files</p>
        </div>
        <button className="btn-primary">Build</button>
      </div>
      
      <div className="panel p-4">
        <h3 className="font-semibold mb-3">Files</h3>
        <div className="text-zinc-400 text-sm">Loading files...</div>
      </div>
    </div>
  )
}