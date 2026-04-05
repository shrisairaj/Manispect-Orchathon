import React from 'react';
import { Outlet } from 'react-router-dom';
import { Calculator } from 'lucide-react';

export default function AuthLayout() {
  return (
    <div className="auth-container">
      <div className="auth-card glass-panel animate-fade-in">
        <div className="auth-header">
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem', color: 'var(--primary-color)' }}>
            <Calculator size={48} />
          </div>
          <h1 className="auth-title">QuantSolve</h1>
          <p className="auth-subtitle">Advanced Algebraic Engine</p>
        </div>
        <Outlet />
      </div>
    </div>
  );
}
