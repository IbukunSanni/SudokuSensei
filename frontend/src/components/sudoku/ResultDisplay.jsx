import SudokuGrid from './SudokuGrid';

/**
 * Renders the error result section
 */
function ErrorResult({ errorResult }) {
  const titleStyle = {
    color: "#f44336",
    marginBottom: "1rem",
  };
  
  const messageStyle = {
    color: "#666",
    marginBottom: "1rem",
    fontSize: "1.1rem",
  };
  
  const suggestionsContainerStyle = {
    backgroundColor: "#fff3cd",
    border: "1px solid #ffeaa7",
    borderRadius: "5px",
    padding: "1rem",
    margin: "1rem 0",
    textAlign: "left",
  };
  
  const suggestionsHeaderStyle = {
    color: "#856404",
    marginBottom: "0.5rem",
  };
  
  const suggestionsListStyle = {
    color: "#856404",
    margin: 0,
    paddingLeft: "1.5rem",
  };
  
  const suggestionItemStyle = {
    marginBottom: "0.25rem",
  };
  
  return (
    <div>
      <h2 style={titleStyle}>
        ❌{" "}
        {errorResult.error_type === "NO_SOLUTION"
          ? "Not Solvable"
          : "Invalid Puzzle"}
      </h2>
      <p style={messageStyle}>
        {errorResult.message}
      </p>
      {errorResult.suggestions && errorResult.suggestions.length > 0 && (
        <div style={suggestionsContainerStyle}>
          <h4 style={suggestionsHeaderStyle}>
            💡 Suggestions:
          </h4>
          <ul style={suggestionsListStyle}>
            {errorResult.suggestions.map((suggestion, idx) => (
              <li key={idx} style={suggestionItemStyle}>
                {suggestion}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

/**
 * Renders the success result section
 */
function SuccessResult({ successResult }) {
  const titleStyle = {
    marginBottom: "1rem",
    color: successResult.is_solved ? "#4CAF50" : "#ff9800",
  };
  
  const messageStyle = {
    color: "#666",
    marginBottom: "1.5rem",
    fontStyle: "italic",
  };

  const stepContainerStyle = {
    margin: "2rem 0",
    textAlign: "left",
  };

  const stepTitleStyle = {
    fontWeight: "bold",
    marginBottom: "0.5rem",
    color: "#1976d2",
  };

  const stepDescStyle = {
    marginBottom: "0.5rem",
    color: "#333",
  };

  return (
    <div>
      <h2 style={titleStyle}>
        {successResult.is_solved
          ? "✅ Solution Found!"
          : "⚠️ Partial Solution"}
      </h2>
      <p style={messageStyle}>
        {successResult.message}
      </p>

      <SudokuGrid 
        puzzle={successResult.solved_grid}
        isReadOnly={true}
        solvedGrid={successResult.solved_grid}
        isSolved={successResult.is_solved}
      />

      {/* Show step-by-step process if available */}
      {successResult.solving_steps && successResult.solving_steps.length > 0 && (
        <div style={stepContainerStyle}>
          <h3>Solving Steps</h3>
          {successResult.solving_steps.map((step, idx) => (
            <div key={idx} style={{marginBottom: '2rem', border: '1px solid #eee', borderRadius: 8, padding: '1rem', background: '#fafbfc'}}>
              <div style={stepTitleStyle}>Step {idx + 1}: {step.technique}</div>
              <div style={stepDescStyle}>{step.description}</div>
              <SudokuGrid puzzle={step.grid} isReadOnly={true} />
              {step.explanation && (
                <div style={{color: '#555', fontSize: '0.95rem', marginTop: '0.5rem'}}>
                  <strong>Explanation:</strong> {step.explanation}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

/**
 * Component to display solving results
 */
export default function ResultDisplay({ result }) {
  if (!result) return null;
  
  const containerStyle = {
    textAlign: "center",
  };
  
  return (
    <div style={containerStyle}>
      {result.error 
        ? <ErrorResult errorResult={result} /> 
        : <SuccessResult successResult={result} />
      }
    </div>
  );
}