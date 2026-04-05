import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { Calculator, LayoutDashboard, User, LogOut } from 'lucide-react';

export default function MainLayout({ onLogout }) {
  const location = useLocation();

  return (
    <div className="main-layout">
      <nav className="navbar">
        <Link to="/dashboard" className="nav-brand">
          <Calculator size={28} color="var(--primary-color)" />
          QuantSolve
        </Link>
        <div className="nav-links">
          <Link 
            to="/dashboard" 
            className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <LayoutDashboard size={20} />
            Dashboard
          </Link>
          <Link 
            to="/profile" 
            className={`nav-link ${location.pathname === '/profile' ? 'active' : ''}`}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <User size={20} />
            Profile
          </Link>
          <button 
            onClick={onLogout}
            style={{ 
              background: 'transparent', 
              border: 'none', 
              color: 'var(--text-muted)', 
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              fontSize: '1rem',
              padding: '0.5rem'
            }}
            onMouseOver={(e) => e.currentTarget.style.color = 'var(--danger-color)'}
            onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
          >
            <LogOut size={20} />
            Logout
          </button>
        </div>
      </nav>
      <main className="page-container animate-fade-in">
        <Outlet />
      </main>
    </div>
  );
}
