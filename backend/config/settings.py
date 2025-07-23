"""
Application configuration settings
"""

from typing import List


class Settings:
    """Application settings"""

    # API Configuration
    API_TITLE: str = "SudokuSensei API"
    API_VERSION: str = "1.0"
    API_DESCRIPTION: str = "An educational Sudoku solver with step-by-step explanations"

    # CORS Configuration
    CORS_ORIGINS: List[str] = [
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


# Global settings instance
settings = Settings()
