/**
 * 📐 Sidebar Component
 */

import React from 'react';


const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: 'home' },
  { id: 'projects', label: 'Projects', icon: 'folder' },
  { id: 'templates', label: 'Templates', icon: 'layout' },
  { id: 'create', label: 'Create New', icon: 'plus' },
  { id: 'sandbox', label: 'Sandbox', icon: 'box' },
];


const icons = {
  home: (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
      <polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
  ),
  folder: (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
    </svg>
  ),
  layout: (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
      <line x1="3" y1="9" x2="21" y2="9"/>
      <line x1="9" y1="21" x2="9" y2="9"/>
    </svg>
  ),
  plus: (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="5" x2="12" y2="19"/>
      <line x1="5" y1="12" x2="19" y2="12"/>
    </svg>
  ),
  box: (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
      <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
      <line x1="12" y1="22.08" x2="12" y2="12"/>
    </svg>
  ),
};


export default function Sidebar({ currentPage, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polygon points="12 2 2 7 12 12 22 7 12 2"/>
            <polyline points="2 17 12 22 22 17"/>
            <polyline points="2 12 12 17 22 12"/>
          </svg>
        </div>
        <span className="logo-text">Factory</span>
      </div>
      
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            <span className="nav-icon">{icons[item.icon]}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <div className="footer-stats">
          <div className="stat">
            <span className="stat-value">12</span>
            <span className="stat-label">Projects</span>
          </div>
          <div className="stat">
            <span className="stat-value">48</span>
            <span className="stat-label">Templates</span>
          </div>
        </div>
      </div>
      
      <style>{`
        .sidebar {
          width: 240px;
          height: 100vh;
          background: var(--bg-secondary);
          border-right: 1px solid var(--border-color);
          display: flex;
          flex-direction: column;
          position: sticky;
          top: 0;
          flex-shrink: 0;
        }
        
        .sidebar-logo {
          display: flex;
          align-items: center;
          gap: var(--space-sm);
          padding: var(--space-lg);
          border-bottom: 1px solid var(--border-color);
        }
        
        .logo-icon {
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
          border-radius: var(--radius-md);
          color: white;
        }
        
        .logo-text {
          font-size: 1.125rem;
          font-weight: 700;
        }
        
        .sidebar-nav {
          flex: 1;
          padding: var(--space-md);
          display: flex;
          flex-direction: column;
          gap: var(--space-xs);
        }
        
        .nav-item {
          display: flex;
          align-items: center;
          gap: var(--space-sm);
          padding: var(--space-sm) var(--space-md);
          background: none;
          border: none;
          border-radius: var(--radius-md);
          color: var(--text-secondary);
          font-size: 0.875rem;
          cursor: pointer;
          transition: all var(--transition-fast);
          text-align: left;
        }
        
        .nav-item:hover {
          background: var(--bg-tertiary);
          color: var(--text-primary);
        }
        
        .nav-item.active {
          background: rgba(99, 102, 241, 0.1);
          color: var(--accent-primary);
        }
        
        .nav-icon {
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .nav-label {
          font-weight: 500;
        }
        
        .sidebar-footer {
          padding: var(--space-md);
          border-top: 1px solid var(--border-color);
        }
        
        .footer-stats {
          display: flex;
          justify-content: space-around;
        }
        
        .stat {
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        
        .stat-value {
          font-size: 1.25rem;
          font-weight: 700;
          color: var(--accent-primary);
        }
        
        .stat-label {
          font-size: 0.75rem;
          color: var(--text-tertiary);
        }
        
        @media (max-width: 768px) {
          .sidebar {
            width: 64px;
          }
          
          .nav-label,
          .logo-text,
          .footer-stats {
            display: none;
          }
        }
      `}</style>
    </aside>
  );
}