"""
Application configuration settings
"""

import os
from typing import List


class Settings:
    """Application settings"""

    # API Configuration
    API_TITLE: str = "SudokuSensei API"
    API_VERSION: str = "1.0"
    API_DESCRIPTION: str = "An educational Sudoku solver with step-by-step explanations"

    # CORS Configuration - Environment aware
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Get CORS origins based on environment"""
        if os.getenv("VERCEL_ENV"):  # Running on Vercel
            return ["*"]  # Allow all origins in production
        else:  # Local development
            return [
                "http://localhost:3000",
                "http://localhost:3001",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
            ]

    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Server Configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True

    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    # Sudoku Solver Configuration
    SUDOKU_MAX_ITERATIONS: int = 100  # Default max iterations for all solvers


# Global settings instance
settings = Settings()

# Auto-deployment test #2: Testing Vercel Git integration workflow
