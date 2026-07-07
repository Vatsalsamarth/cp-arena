from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "CP Arena"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    DATABASE_URL: str
    REDIS_URL: str

    DISCORD_BOT_TOKEN: str

    # Authentication
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()