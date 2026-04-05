import { useState } from 'react'

function InputForm({ onSolve, loading }) {
  const [expression, setExpression] = useState('10a + 15b + 20c + 50d + 5e = 1000')
  const [constraints, setConstraints] = useState(['a >= 2', 'b <= 10'])

  const handleSubmit = (e) => {
    e.preventDefault()
    onSolve(expression, constraints.filter(c => c.trim()))
  }

  const addConstraint = () => {
    setConstraints([...constraints, ''])
  }

  const updateConstraint = (index, value) => {
    const newConstraints = [...constraints]
    newConstraints[index] = value
    setConstraints(newConstraints)
  }

  const removeConstraint = (index) => {
    setConstraints(constraints.filter((_, i) => i !== index))
  }

  return (
    <form onSubmit={handleSubmit} className="input-form">
      <div className="form-group">
        <label>Equation:</label>
        <input
          type="text"
          value={expression}
          onChange={(e) => setExpression(e.target.value)}
          placeholder="e.g., 10a + 15b + 20c + 50d + 5e = 1000"
        />
      </div>

      <div className="form-group">
        <label>Constraints:</label>
        {constraints.map((constraint, index) => (
          <div key={index} className="constraint-row">
            <input
              type="text"
              value={constraint}
              onChange={(e) => updateConstraint(index, e.target.value)}
              placeholder="e.g., a >= 2"
            />
            <button type="button" onClick={() => removeConstraint(index)}>Remove</button>
          </div>
        ))}
        <button type="button" onClick={addConstraint}>Add Constraint</button>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Solving...' : 'Solve'}
      </button>
    </form>
  )
}

export default InputForm
