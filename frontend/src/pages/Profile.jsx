import React, { useState } from 'react';
import { User, Settings, Save, Bell } from 'lucide-react';
import { Input } from '../components/Input';
import { Button } from '../components/Button';

export default function Profile() {
  const [isSaving, setIsSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const handleSave = (e) => {
    e.preventDefault();
    setIsSaving(true);
    setSuccessMsg('');
    
    setTimeout(() => {
      setIsSaving(false);
      setSuccessMsg('Profile configuration updated successfully.');
      setTimeout(() => setSuccessMsg(''), 3000);
    }, 1200);
  };

  return (
    <div className="profile-section animate-fade-in">
      <h1 style={{ fontSize: '2rem', marginBottom: '2rem' }}>Account Settings</h1>
      
      <div className="glass-panel" style={{ padding: '2rem' }}>
        <div className="profile-avatar">
          <User size={48} color="var(--primary-color)" />
        </div>
        
        <h2 style={{ textAlign: 'center', fontSize: '1.25rem', marginBottom: '2rem' }}>Developer Profile</h2>
        
        {successMsg && (
          <div className="animate-fade-in" style={{ padding: '0.75rem 1rem', background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', border: '1px solid currentColor', borderRadius: '8px', marginBottom: '1.5rem', textAlign: 'center', fontWeight: 500 }}>
            {successMsg}
          </div>
        )}

        <form onSubmit={handleSave}>
          <div className="form-group" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', flexDirection: 'row' }}>
            <Input label="First Name" defaultValue="Demo" />
            <Input label="Last Name" defaultValue="User" />
          </div>
          
          <Input label="Email Architecture" type="email" defaultValue="demo@quantsolve.com" readOnly style={{ opacity: 0.7 }} />
          
          <div style={{ marginTop: '2rem', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
            <h3 style={{ fontSize: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Settings size={18} color="var(--primary-color)" /> Preferences
            </h3>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', padding: '0.5rem 0' }}>
            <div>
              <p style={{ fontWeight: 500 }}>Render Telemetry Alerts</p>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Receive notifications on slow equation processing.</p>
            </div>
            <div style={{ width: '40px', height: '24px', background: 'var(--primary-color)', borderRadius: '12px', position: 'relative', cursor: 'pointer' }}>
              <div style={{ width: '18px', height: '18px', background: 'white', borderRadius: '50%', position: 'absolute', top: '3px', right: '3px' }}></div>
            </div>
          </div>
          
          <div style={{ marginTop: '2.5rem' }}>
            <Button type="submit" isLoading={isSaving}>
              <Save size={18} /> Apply Changes
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
