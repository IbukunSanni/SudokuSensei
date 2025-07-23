"""
Main entry point for the SudokuSensei backend application.
This file imports the app instance from app.py and serves as the entry point for running the server.
"""

import uvicorn
from app import app

# This file is kept for backward compatibility
# The actual application is now defined in app.py

if __name__ == "__main__":
    # Run the application using uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
