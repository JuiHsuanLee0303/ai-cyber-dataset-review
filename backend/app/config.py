from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rejection_threshold: int = 3
    approval_threshold: int = 2
    ollama_model: str = "qwen3:1.7b"
    ollama_url: str = "http://host.docker.internal:11434"

    # JWT settings
    secret_key: str = "a_very_secret_key_that_should_be_in_env_file"
    refresh_secret_key: str = "a_different_very_secret_key_for_refresh"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7


    class Config:
        # If you were loading from a .env file, you would specify it here
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single, reusable instance of the settings
settings = Settings() 