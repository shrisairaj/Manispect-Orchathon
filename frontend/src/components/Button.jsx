import React from 'react';

export function Button({ children, isLoading, ...props }) {
  return (
    <button className="btn" disabled={isLoading} {...props}>
      {isLoading && <div className="spinner"></div>}
      {children}
    </button>
  );
}
