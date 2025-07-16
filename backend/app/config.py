from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rejection_threshold: int = 3
    ollama_model: str = "llama3"
    ollama_url: str = "http://host.docker.internal:11434"

    class Config:
        # If you were loading from a .env file, you would specify it here
        # env_file = ".env"
        pass

# Create a single, reusable instance of the settings
settings = Settings() 