import { useState } from 'react'
import './App.css'
import InputForm from './components/InputForm.jsx'
import ResultPanel from './components/ResultPanel.jsx'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSolve = async (expression, constraints) => {
    setLoading(true)
    if (!expression || !expression.trim()) {
      setResults({error: "Please enter an equation"})
      setLoading(false)
      return
    }
    try {
      const response = await fetch('https://your-backend.onrender.com/solve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          expression,
          constraints,
          displayLimit: 10
        }),
      })
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Error:', error)
      setResults({ error: error.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <h1>QuantSolve</h1>
      <InputForm onSolve={handleSolve} loading={loading} />
      <ResultPanel results={results} />
    </div>
  )
}

export default App
