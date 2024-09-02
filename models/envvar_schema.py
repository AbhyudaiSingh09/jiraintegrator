from pydantic_settings import BaseSettings
from pydantic import EmailStr, field_validator

class ENVConfig(BaseSettings):
    EMAIL: EmailStr
    API_TOKEN: str

    @field_validator("API_TOKEN")
    def check_api_token(cls, value):
        if not value:
            raise ValueError("API_TOKEN cannot be empty")
        if len(value) < 20: 
            raise ValueError("API_TOKEN is too short")
        return value

    class Config:
        env_file = ".env"

# Function to load and return the Config object
def load_env_config() -> ENVConfig:
    return ENVConfig()