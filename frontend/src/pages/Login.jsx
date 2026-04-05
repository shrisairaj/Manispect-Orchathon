import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { AlertCircle } from 'lucide-react';
import { Input } from '../components/Input';
import { Button } from '../components/Button';

export default function Login({ onLogin }) {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [authError, setAuthError] = useState('');

  const validate = () => {
    const newErrors = {};
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAuthError('');
    if (!validate()) return;
    
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      if (formData.email === 'demo@quantsolve.com') {
        onLogin();
      } else {
        setAuthError('Invalid credentials. Use demo@quantsolve.com');
      }
    }, 1500);
  };

  return (
    <form onSubmit={handleSubmit}>
      {authError && (
        <div style={{ marginBottom: '1.25rem', padding: '0.75rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger-color)', borderRadius: '8px', color: 'var(--danger-color)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertCircle size={18} />
          <span>{authError}</span>
        </div>
      )}
      
      <Input 
        label="Email Address" 
        type="email" 
        placeholder="demo@quantsolve.com"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        error={errors.email}
      />
      
      <Input 
        label="Password" 
        type="password" 
        placeholder="••••••••"
        value={formData.password}
        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        error={errors.password}
      />
      
      <div style={{ marginTop: '2rem' }}>
        <Button type="submit" isLoading={isLoading}>
          Sign In Target
        </Button>
      </div>
      
      <p style={{ marginTop: '1.5rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        Don't have an account?{' '}
        <Link to="/signup" style={{ fontWeight: 500 }}>Create one</Link>
      </p>
    </form>
  );
}
