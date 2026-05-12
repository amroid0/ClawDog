from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    workspace_path: str = "default-workspace"
    workspace_file_name: str = "user.config.yaml"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

def get_settings() -> Settings:
    return Settings()