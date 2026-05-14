import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function Home() {
  return (
    <div className="page">
      <h1>Welcome to My App</h1>
      <p>Start building your amazing project!</p>
      <Link to="/login" className="btn">Get Started</Link>
    </div>
  );
}

function Login() {
  return (
    <div className="page">
      <h2>Login</h2>
      <form>
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

function Dashboard() {
  return (
    <div className="page">
      <h1>Dashboard</h1>
      <p>Welcome back!</p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
