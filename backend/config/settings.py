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
        """Return explicit browser origins; never combine credentials with '*'."""
        configured = os.getenv("CORS_ORIGINS", "")
        if configured.strip():
            return [
                origin.strip().rstrip("/")
                for origin in configured.split(",")
                if origin.strip()
            ]
        if os.getenv("VERCEL_ENV"):
            return ["https://sudoku-sensei.vercel.app"]
        return [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
        ]

    @property
    def CORS_ORIGIN_REGEX(self) -> str | None:
        """Allow this project's Vercel preview URLs without opening all origins."""
        configured = os.getenv("CORS_ORIGIN_REGEX")
        if configured:
            return configured
        if os.getenv("VERCEL_ENV"):
            return r"https://sudoku-sensei(?:-[a-z0-9-]+)?\.vercel\.app"
        return None

    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Server Configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True

    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    @property
    def ENVIRONMENT(self) -> str:
        return os.getenv("VERCEL_ENV") or os.getenv("ENVIRONMENT", "development")

    # Sudoku Solver Configuration
    SUDOKU_MAX_ITERATIONS: int = 100  # Default max iterations for all solvers


# Global settings instance
settings = Settings()

# Auto-deployment test #2: Testing Vercel Git integration workflow
