function ResultPanel({ results }) {
  if (!results) {
    return <div className="result-panel">Enter an equation and click Solve to see results.</div>
  }

  if (results.error) {
    return <div className="result-panel error">Error: {results.error}</div>
  }

  return (
    <div className="result-panel">
      <h2>Results</h2>
      <p>Total solutions: {results.totalSolutions}</p>
      <p>Shown solutions: {results.shownSolutions}</p>

      {results.solutions && results.solutions.length > 0 && (
        <div className="solutions">
          <h3>Solutions:</h3>
          {results.solutions.map((solution, index) => (
            <div key={index} className="solution">
              {Object.entries(solution).map(([variable, val]) => (
                <span key={variable}>{variable}: {val}</span>
              )).reduce((prev, curr) => [prev, ', ', curr])}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ResultPanel
