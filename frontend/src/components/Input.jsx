import React from 'react';

export function Input({ label, error, ...props }) {
  return (
    <div className="form-group">
      {label && <label className="form-label">{label}</label>}
      <input 
        className={`input-field ${error ? 'error' : ''}`} 
        {...props} 
      />
      {error && <span className="error-text">{error}</span>}
    </div>
  );
}
