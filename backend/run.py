"""
Script to run the SudokuSensei backend server.
"""

import uvicorn
from config.settings import settings

if __name__ == "__main__":
    print(f"Starting SudokuSensei API on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
