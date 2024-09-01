from pydantic_settings import BaseSettings
from pydantic import EmailStr, field_validator
from dotenv import load_dotenv
import yaml


# Load environment variables from .env file
load_dotenv()

class Config(BaseSettings):
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
        
config = Config()


def load_yaml_config(file_path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data

yaml_config = load_yaml_config("config/config.yaml")
