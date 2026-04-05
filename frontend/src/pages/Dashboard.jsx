import React, { useState } from 'react';
import { FunctionSquare, Activity, ChevronRight, Hash } from 'lucide-react';
import { Input } from '../components/Input';
import { Button } from '../components/Button';

export default function Dashboard() {
  const [equation, setEquation] = useState('2x + 5 = 15');
  const [constraint, setConstraint] = useState('x > 0');
  const [isSolving, setIsSolving] = useState(false);
  const [result, setResult] = useState(null);

  const handleSolve = (e) => {
    e.preventDefault();
    if (!equation) return;

    setIsSolving(true);
    setResult(null);

    // Simulate complex computation
    setTimeout(() => {
      setIsSolving(false);
      setResult([
        { step: 'Subtract 5 from both sides', eq: '2x = 10' },
        { step: 'Divide both sides by 2', eq: 'x = 5' }
      ]);
    }, 2000);
  };

  return (
    <div>
      <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>Workspace</h1>
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>Define your mathematical constraints and execute algebraic reductions.</p>

      <div className="dashboard-grid">
        {/* Solver Panel */}
        <div className="glass-panel dashboard-card">
          <h2 className="card-title">
            <FunctionSquare size={24} color="var(--primary-color)" />
            Solver Engine
          </h2>

          <form onSubmit={handleSolve} style={{ marginTop: '1.5rem' }}>
            <Input
              label="Equation Context"
              value={equation}
              onChange={(e) => setEquation(e.target.value)}
              placeholder="e.g. 2x^2 + 5x - 3 = 0"
            />

            <Input
              label="Constraints (Optional)"
              value={constraint}
              onChange={(e) => setConstraint(e.target.value)}
              placeholder="e.g. x ∈ ℝ"
            />

            <div style={{ marginTop: '1.5rem' }}>
              <Button type="submit" isLoading={isSolving}>
                Execute Calculation
              </Button>
            </div>
          </form>
        </div>

        {/* Results Panel */}
        <div className="glass-panel dashboard-card">
          <h2 className="card-title">
            <Activity size={24} color="var(--primary-color)" />
            Execution Output
          </h2>

          <div style={{ marginTop: '1.5rem', minHeight: '200px', display: 'flex', flexDirection: 'column' }}>
            {isSolving ? (
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
                <div className="spinner" style={{ width: '30px', height: '30px', margin: '0 auto 1rem', borderTopColor: 'var(--primary-color)' }}></div>
                <p className="animate-fade-in">Compiling syntax tree...</p>
              </div>
            ) : result ? (
              <div className="animate-fade-in">
                <div style={{ background: 'rgba(59, 130, 246, 0.1)', padding: '1rem', borderRadius: '8px', borderLeft: '4px solid var(--primary-color)', marginBottom: '1.5rem' }}>
                  <p style={{ fontWeight: 600, color: 'var(--primary-color)' }}>Solution Validated</p>
                  <p style={{ fontSize: '1.5rem', fontWeight: 700, marginTop: '0.25rem' }}>x = 5</p>
                </div>

                <h3 style={{ fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '1px', color: 'var(--text-muted)', marginBottom: '1rem' }}>Resolution Steps</h3>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {result.map((step, idx) => (
                    <div key={idx} style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '24px', height: '24px', borderRadius: '50%', background: 'rgba(255,255,255,0.1)', fontSize: '0.75rem', fontWeight: 600 }}>{idx + 1}</div>
                      <div>
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '0.25rem' }}>{step.step}</p>
                        <p style={{ fontFamily: 'monospace', fontWeight: 500, fontSize: '1rem' }}>{step.eq}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', textAlign: 'center', border: '1px dashed var(--border-color)', borderRadius: '8px' }}>
                <p>Awaiting payload processing...<br />Run a calculation to view the AST and output.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
