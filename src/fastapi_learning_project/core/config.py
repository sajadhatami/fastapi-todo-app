from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """
    Settings class for application configuration.
    """
    
    DATABASE_URL: str
    
    
    # ConfigDict: IS AN CLASS THAT ALLOWS YOU TO DEFINE 
    # CONFIGURATION OPTIONS FOR THE SETTINGS CLASS. 
    # IT efects all the attributes of the Settings class
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  
    )

settings = Settings()