from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    MAILTRAP_USERNAME: str
    MAILTRAP_PASSWORD: str
    MAILTRAP_PORT: str
    APP_EMAIL:str



    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()