# SudokuSensei

An educational Sudoku solver that highlights rule violations and provides step-by-step solving explanations.

## Project Structure

- **Backend**: Python FastAPI application with advanced Sudoku solving algorithms
- **Frontend**: React/Next.js application with an interactive Sudoku board

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```
   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```
   
   Or use the provided batch file:
   ```
   start-dev.bat
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies (use the setup script):
   ```
   setup.bat
   ```
   
   Or manually:
   ```
   npm install --no-save
   ```

3. Start the development server:
   ```
   start-dev.bat
   ```
   
   Or manually:
   ```
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Features

- Interactive Sudoku board with real-time validation
- Highlights duplicate numbers and affected rows/columns/boxes
- Solves puzzles using advanced techniques:
  - Naked singles
  - Hidden singles
  - Hidden pairs
  - Naked pairs
- Provides detailed feedback on solving process
- Load example puzzles or create your own

## API Endpoints

- `GET /`: Health check
- `GET /health`: Detailed service status
- `POST /solve`: Solve a Sudoku puzzle

## Technologies Used

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: React, Next.js
- **Styling**: Pure inline styles for all components