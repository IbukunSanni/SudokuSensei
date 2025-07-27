import axios from "axios";

// API endpoint configuration
const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL_IP ||
  process.env.NEXT_PUBLIC_BACKEND_URL_LOCALHOST;

/**
 * Service for API interactions
 */
const apiService = {
  /**
   * Sends the puzzle to the backend for complete solving
   *
   * This function calls the /solve endpoint which applies all available techniques
   * until the puzzle is solved or no more progress can be made.
   *
   * @param {number[][]} puzzle - 9x9 Sudoku grid where 0 represents empty cells
   * @returns {Promise<Object>} Promise with the complete solution data containing:
   *   - solved_grid: The final solved grid
   *   - solving_steps: Array of all steps taken during solving
   *   - techniques_applied: Array of all techniques used
   *   - is_solved: Boolean indicating if puzzle was completely solved
   *   - message: Status message about the solving process
   */
  solvePuzzle: async (puzzle) => {
    try {
      const response = await axios.post(`${BACKEND_URL}/solve`, { puzzle });
      return response.data;
    } catch (error) {
      const errorData = error.response?.data?.detail;
      if (errorData && typeof errorData === "object") {
        // Structured error from backend
        return {
          error: true,
          error_type: errorData.error_type,
          message: errorData.message,
          suggestions: errorData.suggestions || [],
        };
      } else {
        // Fallback for other errors
        return {
          error: true,
          error_type: "UNKNOWN_ERROR",
          message: error.response?.data?.detail || error.message,
          suggestions: ["Please try again or check your network connection"],
        };
      }
    }
  },

  /**
   * Applies a single solving step to the puzzle for educational step-by-step learning
   *
   * This function calls the /solve-step endpoint which applies only one technique
   * and returns detailed information for visual highlighting and learning.
   *
   * @param {number[][]} puzzle - 9x9 Sudoku grid where 0 represents empty cells
   * @returns {Promise<Object>} Promise with the single step result containing:
   *   - solved_grid: Updated grid after applying one technique
   *   - solving_steps: Array with one step containing:
   *     - focus_cells: Array of [row, col] coordinates for green highlighting
   *     - technique: Name of the technique applied (e.g., "Naked Single")
   *     - description: Human-readable explanation of what happened
   *     - solved_positions: Array of solved cell positions (e.g., ["C1=7"])
   *     - value: The value that was placed (if any)
   *   - techniques_applied: Array of technique names used
   *   - is_solved: Boolean indicating if puzzle is completely solved
   */
  applySingleStep: async (puzzle) => {
    try {
      const response = await axios.post(`${BACKEND_URL}/solve-step`, {
        puzzle,
      });
      return response.data;
    } catch (error) {
      const errorData = error.response?.data?.detail;
      if (errorData && typeof errorData === "object") {
        // Structured error from backend
        return {
          error: true,
          error_type: errorData.error_type,
          message: errorData.message,
          suggestions: errorData.suggestions || [],
        };
      } else {
        // Fallback for other errors
        return {
          error: true,
          error_type: "UNKNOWN_ERROR",
          message: error.response?.data?.detail || error.message,
          suggestions: ["Please try again or check your network connection"],
        };
      }
    }
  },
};

export default apiService;
