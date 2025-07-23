import axios from 'axios';

// API endpoint configuration
const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL_IP ||
  process.env.NEXT_PUBLIC_BACKEND_URL_LOCALHOST;

/**
 * Service for API interactions
 */
const apiService = {
  /**
   * Sends the puzzle to the backend for solving
   * 
   * @param {number[][]} puzzle - 9x9 Sudoku grid
   * @returns {Promise} Promise with the solution data
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
};

export default apiService;