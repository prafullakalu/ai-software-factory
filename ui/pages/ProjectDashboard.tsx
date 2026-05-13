/**
 * 📊 Project Dashboard
 * 
 * Shows all created projects with stats.
 */

import React, { useState } from 'react';


// Mock data for demo
const mockProjects = [
  {
    id: '1',
    name: 'FinTech Payment Gateway',
    description: 'Payment processing with Stripe integration',
    status: 'ready',
    project_type: 'fintech',
    created_at: '2024-01-15',
    files_created: 156,
    lines_of_code: 12450,
  },
  {
    id: '2', 
    name: 'SaaS Dashboard',
    description: 'Analytics dashboard with charts',
    status: 'deployed',
    project_type: 'saas',
    created_at: '2024-01-12',
    files_created: 89,
    lines_of_code: 8320,
  },
  {
    id: '3',
    name: 'E-commerce Store',
    description: 'Online store with cart',
    status: 'generating',
    project_type: 'ecommerce',
    created_at: '2024-01-18',
    files_created: 12,
    lines_of_code: 890,
  },
  {
    id: '4',
    name: 'Banking API',
    description: 'REST API for banking',
    status: 'ready',
    project_type: 'api',
    created_at: '2024-01-10',
    files_created: 45,
    lines_of_code: 4200,
  },
];


const statusColors = {
  draft: 'badge',
  generating: 'badge badge-warning',
  ready: 'badge badge-success',
  deployed: 'badge badge-primary',
  failed: 'badge badge-error',
};

const typeColors = {
  saas: '#6366f1',
  fintech: '#10b981', 
  ecommerce: '#f59e0b',
  api: '#8b5cf6',
  dashboard: '#ec4899',
};


export default function ProjectDashboard({ onSelectProject, onCreate }) {
  const [filter, setFilter] = useState('all');
  
  const filteredProjects = filter === 'all' 
    ? mockProjects 
    : mockProjects.filter(p => p.status === filter);
  
  const stats = {
    total: mockProjects.length,
    ready: mockProjects.filter(p => p.status === 'ready').length,
    deployed: mockProjects.filter(p => p.status === 'deployed').length,
    generating: mockProjects.filter(p => p.status === 'generating').length,
  };
  
  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-secondary mt-sm">Manage your AI-generated projects</p>
        </div>
        <button className="btn btn-primary" onClick={onCreate}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          New Project
        </button>
      </div>
      
      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{background: 'rgba(99, 102, 241, 0.1)'}}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6366f1" strokeWidth="2">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <div className="stat-content">
            <span className="stat-value">{stats.total}</span>
            <span className="stat-label">Total Projects</span>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon" style={{background: 'rgba(16, 185, 129, 0.1)'}}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
          </div>
          <div className="stat-content">
            <span className="stat-value">{stats.ready}</span>
            <span className="stat-label">Ready</span>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon" style={{background: 'rgba(34, 211, 238, 0.1)'}}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" strokeWidth="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
          </div>
          <div className="stat-content">
            <span className="stat-value">{stats.deployed}</span>
            <span className="stat-label">Deployed</span>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon" style={{background: 'rgba(245, 158, 11, 0.1)'}}>
            <div className="spinner" style={{borderTopColor: '#f59e0b'}}/>
          </div>
          <div className="stat-content">
            <span className="stat-value">{stats.generating}</span>
            <span className="stat-label">Generating</span>
          </div>
        </div>
      </div>
      
      {/* Filter */}
      <div className="filter-bar">
        <button 
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Projects
        </button>
        <button 
          className={`filter-btn ${filter === 'ready' ? 'active' : ''}`}
          onClick={() => setFilter('ready')}
        >
          Ready
        </button>
        <button 
          className={`filter-btn ${filter === 'generating' ? 'active' : ''}`}
          onClick={() => setFilter('generating')}
        >
          Generating
        </button>
        <button 
          className={`filter-btn ${filter === 'deployed' ? 'active' : ''}`}
          onClick={() => setFilter('deployed')}
        >
          Deployed
        </button>
      </div>
      
      {/* Projects Grid */}
      <div className="projects-grid">
        {filteredProjects.map((project) => (
          <div 
            key={project.id} 
            className="project-card"
            onClick={() => onSelectProject(project)}
          >
            <div className="project-header">
              <div 
                className="project-type-dot"
                style={{background: typeColors[project.project_type]}}
              />
              <span className={statusColors[project.status]}>
                {project.status}
              </span>
            </div>
            
            <h3 className="project-name">{project.name}</h3>
            <p className="project-description">{project.description}</p>
            
            <div className="project-stats">
              <div className="project-stat">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
                <span>{project.files_created} files</span>
              </div>
              <div className="project-stat">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="16" y1="18" x2="16" y2="12"/>
                  <line x1="8" y1="18" x2="8" y2="12"/>
                  <line x1="12" y1="16" x2="12" y2="8"/>
                </svg>
                <span>{project.lines_of_code.toLocaleString()} LOC</span>
              </div>
            </div>
          </div>
        ))}
        
        {/* Empty state / Add new */}
        <div className="project-card new-project" onClick={onCreate}>
          <div className="new-project-content">
            <div className="new-project-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
            </div>
            <span>Create New Project</span>
          </div>
        </div>
      </div>
      
      <style>{`
        .dashboard {
          max-width: 1200px;
          margin: 0 auto;
        }
        
        .dashboard-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: var(--space-xl);
        }
        
        .stats-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: var(--space-md);
          margin-bottom: var(--space-xl);
        }
        
        @media (max-width: 768px) {
          .stats-grid {
            grid-template-columns: repeat(2, 1fr);
          }
        }
        
        .stat-card {
          display: flex;
          align-items: center;
          gap: var(--space-md);
          padding: var(--space-lg);
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-lg);
        }
        
        .stat-icon {
          width: 48px;
          height: 48px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: var(--radius-md);
        }
        
        .stat-content {
          display: flex;
          flex-direction: column;
        }
        
        .stat-value {
          font-size: 1.5rem;
          font-weight: 700;
        }
        
        .stat-label {
          font-size: 0.875rem;
          color: var(--text-secondary);
        }
        
        .filter-bar {
          display: flex;
          gap: var(--space-sm);
          margin-bottom: var(--space-lg);
          padding-bottom: var(--space-md);
          border-bottom: 1px solid var(--border-color);
        }
        
        .filter-btn {
          padding: var(--space-sm) var(--space-md);
          background: none;
          border: none;
          border-radius: var(--radius-md);
          color: var(--text-secondary);
          font-size: 0.875rem;
          cursor: pointer;
          transition: all var(--transition-fast);
        }
        
        .filter-btn:hover {
          color: var(--text-primary);
        }
        
        .filter-btn.active {
          background: var(--bg-tertiary);
          color: var(--text-primary);
        }
        
        .projects-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: var(--space-md);
        }
        
        .project-card {
          padding: var(--space-lg);
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-lg);
          cursor: pointer;
          transition: all var(--transition-fast);
        }
        
        .project-card:hover {
          border-color: var(--border-hover);
          transform: translateY(-2px);
        }
        
        .project-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: var(--space-sm);
        }
        
        .project-type-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
        }
        
        .project-name {
          font-size: 1rem;
          font-weight: 600;
          margin-bottom: var(--space-xs);
        }
        
        .project-description {
          font-size: 0.8125rem;
          color: var(--text-secondary);
          margin-bottom: var(--space-md);
        }
        
        .project-stats {
          display: flex;
          gap: var(--space-md);
          padding-top: var(--space-md);
          border-top: 1px solid var(--border-color);
        }
        
        .project-stat {
          display: flex;
          align-items: center;
          gap: var(--space-xs);
          font-size: 0.75rem;
          color: var(--text-tertiary);
        }
        
        .new-project {
          border-style: dashed;
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 180px;
        }
        
        .new-project-content {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: var(--space-md);
          color: var(--text-tertiary);
        }
        
        .new-project-icon {
          width: 48px;
          height: 48px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--bg-tertiary);
          border-radius: var(--radius-md);
        }
      `}</style>
    </div>
  );
}