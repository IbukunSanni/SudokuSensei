/**
 * Button component with Tailwind styling
 * 
 * @param {Object} props - Component props
 * @param {string} props.text - Button text
 * @param {string} props.color - Button color theme ('green', 'red', or 'blue')
 * @param {Function} props.onClick - Click handler
 * @param {boolean} props.disabled - Whether button is disabled
 * @returns {JSX.Element} Styled button
 */
export default function ActionButton({ text, color, onClick, disabled = false }) {
  // Base classes that apply to all buttons
  let className = "px-6 py-3 text-base font-medium text-white rounded-md transition-colors duration-200";
  
  // Add color-specific classes
  if (disabled) {
    className += " bg-gray-400 cursor-not-allowed";
  } else {
    switch (color) {
      case 'green':
        className += " bg-green-500 hover:bg-green-600";
        break;
      case 'red':
        className += " bg-red-500 hover:bg-red-600";
        break;
      case 'blue':
      default:
        className += " bg-blue-500 hover:bg-blue-600";
        break;
    }
  }
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={className}
    >
      {text}
    </button>
  );
}