/**
 * ➕ Create Project Page
 * 
 * Form to create new SaaS/Fintech projects.
 */

import React, { useState } from 'react';


const projectTypes = [
  { id: 'saas', label: 'SaaS Application', description: 'Complete SaaS with auth, billing, dashboard', icon: 'app' },
  { id: 'fintech', label: 'Fintech App', description: 'Payment processing, wallets, banking', icon: 'finance' },
  { id: 'ecommerce', label: 'E-commerce', description: 'Online store with cart and payments', icon: 'cart' },
  { id: 'api', label: 'REST API', description: 'Backend API with documentation', icon: 'api' },
  { id: 'dashboard', label: 'Dashboard', description: 'Analytics and data visualization', icon: 'chart' },
];


const frontendOptions = [
  { id: 'nextjs', label: 'Next.js', selected: true },
  { id: 'react', label: 'React' },
  { id: 'vue', label: 'Vue.js' },
  { id: 'tailwind', label: 'Tailwind CSS', selected: true },
  { id: 'shadcn', label: 'shadcn/ui' },
];

const backendOptions = [
  { id: 'fastapi', label: 'FastAPI', selected: true },
  { id: 'express', label: 'Express' },
  { id: 'django', label: 'Django' },
  { id: 'nestjs', label: 'NestJS' },
];

const databaseOptions = [
  { id: 'postgresql', label: 'PostgreSQL', selected: true },
  { id: 'mongodb', label: 'MongoDB' },
  { id: 'redis', label: 'Redis' },
  { id: 'supabase', label: 'Supabase' },
];

const features = [
  { id: 'auth', label: 'Authentication', description: 'JWT, OAuth, social login', selected: true },
  { id: 'payments', label: 'Payments', description: 'Stripe, PayPal integration' },
  { id: 'analytics', label: 'Analytics', description: 'Events, metrics, dashboards' },
  { id: 'email', label: 'Email', description: 'Transactional emails' },
  { id: 'files', label: 'File Upload', description: 'S3, Cloud storage' },
  { id: 'realtime', label: 'Real-time', description: 'WebSockets, live updates' },
];


export default function CreateProject({ onCreate }) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    projectType: '',
    frontend: ['nextjs', 'tailwind'],
    backend: ['fastapi'],
    database: ['postgresql'],
    features: ['auth'],
  });
  
  const handleSubmit = () => {
    console.log('Creating project:', formData);
    onCreate();
  };
  
  return (
    <div className="create-project">
      {/* Header */}
      <div className="page-header">
        <button className="btn btn-ghost" onClick={onCreate}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          Back
        </button>
        <h1 className="text-2xl font-bold">Create New Project</h1>
      </div>
      
      {/* Steps */}
      <div className="steps">
        <div className={`step ${step >= 1 ? 'active' : ''}`}>
          <span className="step-number">1</span>
          <span className="step-label">Project Type</span>
        </div>
        <div className="step-connector" />
        <div className={`step ${step >= 2 ? 'active' : ''}`}>
          <span className="step-number">2</span>
          <span className="step-label">Tech Stack</span>
        </div>
        <div className="step-connector" />
        <div className={`step ${step >= 3 ? 'active' : ''}`}>
          <span className="step-number">3</span>
          <span className="step-label">Features</span>
        </div>
      </div>
      
      {/* Step 1: Project Type */}
      {step >= 1 && (
        <div className="step-content">
          <h2 className="step-title">What type of project?</h2>
          <p className="step-description">Select a project template to get started</p>
          
          <div className="type-grid">
            {projectTypes.map((type) => (
              <div 
                key={type.id}
                className={`type-card ${formData.projectType === type.id ? 'selected' : ''}`}
                onClick={() => setFormData({...formData, projectType: type.id})}
              >
                <div className="type-icon">
                  {type.id === 'saas' && '📱'}
                  {type.id === 'fintech' && '💳'}
                  {type.id === 'ecommerce' && '🛒'}
                  {type.id === 'api' && '🔌'}
                  {type.id === 'dashboard' && '📊'}
                </div>
                <h3>{type.label}</h3>
                <p>{type.description}</p>
              </div>
            ))}
          </div>
          
          <div className="form-group">
            <label>Project Name</label>
            <input 
              type="text" 
              className="input"
              placeholder="My Awesome Project"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label>Description</label>
            <textarea 
              className="input textarea"
              placeholder="A brief description of your project"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
            />
          </div>
        </div>
      )}
      
      {/* Step 2: Tech Stack */}
      {step >= 2 && (
        <div className="step-content">
          <h2 className="step-title">Choose your tech stack</h2>
          <p className="step-description">Select the technologies for your project</p>
          
          <div className="stack-section">
            <h3>Frontend</h3>
            <div className="stack-options">
              {frontendOptions.map((opt) => (
                <label key={opt.id} className="stack-option">
                  <input 
                    type="checkbox"
                    checked={formData.frontend.includes(opt.id)}
                    onChange={(e) => {
                      const updated = e.target.checked 
                        ? [...formData.frontend, opt.id]
                        : formData.frontend.filter(f => f !== opt.id);
                      setFormData({...formData, frontend: updated});
                    }}
                  />
                  <span>{opt.label}</span>
                </label>
              ))}
            </div>
          </div>
          
          <div className="stack-section">
            <h3>Backend</h3>
            <div className="stack-options">
              {backendOptions.map((opt) => (
                <label key={opt.id} className="stack-option">
                  <input 
                    type="checkbox"
                    checked={formData.backend.includes(opt.id)}
                    onChange={(e) => {
                      const updated = e.target.checked 
                        ? [...formData.backend, opt.id]
                        : formData.backend.filter(f => f !== opt.id);
                      setFormData({...formData, backend: updated});
                    }}
                  />
                  <span>{opt.label}</span>
                </label>
              ))}
            </div>
          </div>
          
          <div className="stack-section">
            <h3>Database</h3>
            <div className="stack-options">
              {databaseOptions.map((opt) => (
                <label key={opt.id} className="stack-option">
                  <input 
                    type="checkbox"
                    checked={formData.database.includes(opt.id)}
                    onChange={(e) => {
                      const updated = e.target.checked 
                        ? [...formData.database, opt.id]
                        : formData.database.filter(f => f !== opt.id);
                      setFormData({...formData, database: updated});
                    }}
                  />
                  <span>{opt.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      )}
      
      {/* Step 3: Features */}
      {step >= 3 && (
        <div className="step-content">
          <h2 className="step-title">Add features</h2>
          <p className="step-description">Select the features you need</p>
          
          <div className="features-grid">
            {features.map((feature) => (
              <label 
                key={feature.id}
                className={`feature-card ${formData.features.includes(feature.id) ? 'selected' : ''}`}
              >
                <input 
                  type="checkbox"
                  checked={formData.features.includes(feature.id)}
                  onChange={(e) => {
                    const updated = e.target.checked 
                      ? [...formData.features, feature.id]
                      : formData.features.filter(f => f !== feature.id);
                    setFormData({...formData, features: updated});
                  }}
                />
                <div>
                  <h4>{feature.label}</h4>
                  <p>{feature.description}</p>
                </div>
              </label>
            ))}
          </div>
        </div>
      )}
      
      {/* Actions */}
      <div className="step-actions">
        {step > 1 && (
          <button className="btn btn-secondary" onClick={() => setStep(step - 1)}>
            Previous
          </button>
        )}
        
        {step < 3 ? (
          <button 
            className="btn btn-primary" 
            onClick={() => setStep(step + 1)}
            disabled={step === 1 && !formData.projectType}
          >
            Continue
          </button>
        ) : (
          <button 
            className="btn btn-primary" 
            onClick={handleSubmit}
            disabled={!formData.name}
          >
            Create Project
          </button>
        )}
      </div>
      
      <style>{`
        .create-project {
          max-width: 800px;
          margin: 0 auto;
        }
        
        .page-header {
          display: flex;
          align-items: center;
          gap: var(--space-md);
          margin-bottom: var(--space-xl);
        }
        
        .steps {
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: var(--space-2xl);
        }
        
        .step {
          display: flex;
          align-items: center;
          gap: var(--space-sm);
          color: var(--text-tertiary);
        }
        
        .step.active {
          color: var(--text-primary);
        }
        
        .step-number {
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--bg-tertiary);
          border-radius: 50%;
          font-size: 0.875rem;
          font-weight: 600;
        }
        
        .step.active .step-number {
          background: var(--accent-primary);
          color: white;
        }
        
        .step-connector {
          width: 40px;
          height: 2px;
          background: var(--border-color);
          margin: 0 var(--space-sm);
        }
        
        .step-content {
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-lg);
          padding: var(--space-xl);
          margin-bottom: var(--space-lg);
        }
        
        .step-title {
          font-size: 1.25rem;
          font-weight: 600;
          margin-bottom: var(--space-xs);
        }
        
        .step-description {
          color: var(--text-secondary);
          margin-bottom: var(--space-lg);
        }
        
        .type-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
          gap: var(--space-md);
          margin-bottom: var(--space-lg);
        }
        
        .type-card {
          padding: var(--space-lg);
          background: var(--bg-tertiary);
          border: 2px solid transparent;
          border-radius: var(--radius-lg);
          cursor: pointer;
          transition: all var(--transition-fast);
        }
        
        .type-card:hover {
          border-color: var(--border-hover);
        }
        
        .type-card.selected {
          border-color: var(--accent-primary);
          background: rgba(99, 102, 241, 0.1);
        }
        
        .type-icon {
          font-size: 1.5rem;
          margin-bottom: var(--space-sm);
        }
        
        .type-card h3 {
          font-size: 0.9375rem;
          font-weight: 600;
        }
        
        .type-card p {
          font-size: 0.8125rem;
          color: var(--text-secondary);
        }
        
        .form-group {
          margin-bottom: var(--space-md);
        }
        
        .form-group label {
          display: block;
          font-size: 0.875rem;
          font-weight: 500;
          margin-bottom: var(--space-xs);
        }
        
        .stack-section {
          margin-bottom: var(--space-lg);
        }
        
        .stack-section h3 {
          font-size: 0.9375rem;
          font-weight: 600;
          margin-bottom: var(--space-md);
        }
        
        .stack-options {
          display: flex;
          flex-wrap: wrap;
          gap: var(--space-sm);
        }
        
        .stack-option {
          display: flex;
          align-items: center;
          gap: var(--space-sm);
          padding: var(--space-sm) var(--space-md);
          background: var(--bg-tertiary);
          border-radius: var(--radius-md);
          cursor: pointer;
          font-size: 0.875rem;
        }
        
        .stack-option input {
          accent-color: var(--accent-primary);
        }
        
        .features-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: var(--space-md);
        }
        
        .feature-card {
          display: flex;
          align-items: flex-start;
          gap: var(--space-md);
          padding: var(--space-md);
          background: var(--bg-tertiary);
          border: 2px solid transparent;
          border-radius: var(--radius-md);
          cursor: pointer;
        }
        
        .feature-card.selected {
          border-color: var(--accent-primary);
        }
        
        .feature-card input {
          margin-top: 4px;
        }
        
        .feature-card h4 {
          font-size: 0.9375rem;
          font-weight: 600;
        }
        
        .feature-card p {
          font-size: 0.8125rem;
          color: var(--text-secondary);
        }
        
        .step-actions {
          display: flex;
          justify-content: flex-end;
          gap: var(--space-md);
        }
      `}</style>
    </div>
  );
}