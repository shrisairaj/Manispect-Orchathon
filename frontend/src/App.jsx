import { useState } from 'react'
import './App.css'
import InputForm from './components/InputForm'
import ResultPanel from './components/ResultPanel'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSolve = async (expression, constraints) => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:5000/solve', {
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
