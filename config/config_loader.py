from pydantic_settings import BaseSettings
from pydantic import EmailStr
import yaml
from models.config_schemas import AppConfig


def load_yaml_config(file_path: str) -> AppConfig:
    """Load configuration from a YAML file."""
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return AppConfig(**config_data)

yaml_config = load_yaml_config("config/config.yaml")
