from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "CP Arena"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    DATABASE_URL: str
    REDIS_URL: str

    DISCORD_BOT_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
