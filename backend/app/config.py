from pydantic_settings import BaseSettings
import os

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

    # HTTPS settings
    use_https: bool = os.getenv("USE_HTTPS", "false").lower() == "true"
    ssl_cert_file: str = os.getenv("SSL_CERT_FILE", "ssl/certificate.crt")
    ssl_key_file: str = os.getenv("SSL_KEY_FILE", "ssl/private.key")
    https_port: int = int(os.getenv("HTTPS_PORT", "8000"))

    class Config:
        # If you were loading from a .env file, you would specify it here
        env_file = ".env"
        env_file_encoding = 'utf-8'

# 創建全局設置實例
settings = Settings() 