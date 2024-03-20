from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str
    PORT: int
    DEBUG: bool
    CHAT_MS_URL : str

    class Config:
        env_file = ".env"

settings = Settings()