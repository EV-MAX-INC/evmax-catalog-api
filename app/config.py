"""
Configuration settings for the EV MAX Catalog API.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/evmax_catalog"
    
    # API
    api_version: str = "1.0.0"
    api_title: str = "EV MAX Catalog API"
    debug: bool = True
    
    # Business Logic Configuration
    material_markup: float = 0.10  # 10%
    overhead_rate: float = 0.18  # 18%
    ga_excavation_contingency: float = 0.15  # 15%
    target_profit_margin: float = 0.27  # 27%
    roi_analysis_years: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
