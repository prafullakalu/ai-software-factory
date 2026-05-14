import React, { useState } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function Home() {
  return (
    <div className="page">
      <h1>Welcome to FreshApp</h1>
      <p>A beautiful modern application</p>
      <Link to="/app" className="btn">Get Started</Link>
    </div>
  )
}

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  
  const handleSubmit = (e) => {
    e.preventDefault()
    alert(`Login: ${email}`)
  }
  
  return (
    <div className="page">
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        <button type="submit" className="btn">Sign In</button>
      </form>
    </div>
  )
}

function Register() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  
  const handleSubmit = (e) => {
    e.preventDefault()
    alert(`Welcome $FreshApp!`)
  }
  
  return (
    <div className="page">
      <h2>Create Account</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Name" value=FreshApp onChange={e => setName(e.target.value)} />
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        <button type="submit" className="btn">Create Account</button>
      </form>
    </div>
  )
}

function Dashboard() {
  const items = [
    { id: 1, title: 'Dashboard', value: '100', label: 'Total' },
    { id: 2, title: 'Active', value: '45', label: 'Active' },
    { id: 3, title: 'Pending', value: '12', label: 'Pending' },
  ]
  
  return (
    <div className="page">
      <h1>Dashboard</h1>
      <div className="grid">
        {items.map(item => (
          <div key={item.id} className="card">
            <p style={{color: '#888'}}>{item.label}</p>
            <h2>{item.value}</h2>
          </div>
        ))}
      </div>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <div className="navbar">
        <Link to="/" style={{color: '#fff', textDecoration: 'none', fontWeight: 'bold'}}>FreshApp</Link>
        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/app">App</Link>
          <Link to="/login">Login</Link>
        </div>
      </div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/app" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App