"""
Main entry point for the SudokuSensei backend application.

This file serves as the primary entry point for running the FastAPI server.
It imports the app instance from app.py and configures the Uvicorn ASGI server.

Usage:
    python main.py
"""

import uvicorn
from app import app  # Import the FastAPI application instance

# This file is kept for backward compatibility
# The actual application definition and configuration is in app.py

if __name__ == "__main__":
    # This conditional ensures the server only runs when this script is executed directly
    # (not when imported as a module)

    # Configure and run the application using uvicorn (ASGI server)
    uvicorn.run(
        "main:app",  # Path to the app object (format: "module:attribute")
        host="0.0.0.0",  # Host address - 0.0.0.0 makes it accessible from any network interface
        port=8000,  # Port number to run the server on
        reload=True,  # Enable auto-reload on code changes (development mode)
        log_level="info",  # Set logging verbosity level
    )

    # The server will start and listen for incoming HTTP requests
    # API endpoints defined in api/routes.py will be accessible at http://localhost:8000/
    # Swagger UI documentation will be available at http://localhost:8000/docs
    # Auto-deployment test: Updated for Vercel Git integration
