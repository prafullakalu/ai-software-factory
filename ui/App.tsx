/**
 * 💻 APP LAYOUT
 * 
 * Main application layout with sidebar and header.
 */

import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ProjectDashboard from './pages/ProjectDashboard';
import CreateProject from './pages/CreateProject';
import ProjectDetail from './pages/ProjectDetail';
import './styles/globals.css';


/**
 * 🎯 Main App Component
 */
export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [selectedProject, setSelectedProject] = useState(null);
  
  // Render current page
  const renderPage = () => {
    switch (currentPage) {
      case 'create':
        return <CreateProject onCreate={() => setCurrentPage('dashboard')} />;
      case 'project':
        return <ProjectDetail project={selectedProject} onBack={() => setCurrentPage('dashboard')} />;
      default:
        return <ProjectDashboard onSelectProject={(p) => { setSelectedProject(p); setCurrentPage('project'); }} onCreate={() => setCurrentPage('create')} />;
    }
  };
  
  return (
    <div className="app-layout">
      <Sidebar 
        currentPage={currentPage} 
        onNavigate={setCurrentPage} 
      />
      <div className="app-main">
        <Header />
        <main className="app-content">
          {renderPage()}
        </main>
      </div>
      
      <style>{`
        .app-layout {
          display: flex;
          min-height: 100vh;
          background: var(--bg-primary);
        }
        
        .app-main {
          flex: 1;
          display: flex;
          flex-direction: column;
          min-width: 0;
        }
        
        .app-content {
          flex: 1;
          padding: var(--space-xl);
          overflow-y: auto;
        }
        
        @media (max-width: 768px) {
          .app-content {
            padding: var(--space-md);
          }
        }
      `}</style>
    </div>
  );
}