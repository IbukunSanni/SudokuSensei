/**
 * Warning banner for duplicate numbers
 * 
 * @returns {JSX.Element} Warning banner
 */
export default function DuplicateWarning() {
  const containerStyle = {
    backgroundColor: "#ffebee",
    border: "1px solid #f44336",
    borderRadius: "5px",
    padding: "0.75rem",
    margin: "1rem 0",
    textAlign: "center",
  };
  
  const warningTextStyle = {
    fontWeight: "bold",
    color: "#d32f2f",
  };
  
  const descriptionTextStyle = {
    color: "#666",
    marginLeft: "0.5rem",
  };
  
  return (
    <div style={containerStyle}>
      <span style={warningTextStyle}>
        ⚠️ Duplicate numbers detected!
      </span>
      <span style={descriptionTextStyle}>
        Red cells have duplicates, yellow areas show affected
        rows/columns/boxes.
      </span>
    </div>
  );
}