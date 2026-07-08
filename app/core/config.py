from pydantic import ValidationInfo, field_validator
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

    # Request protection
    MAX_REQUEST_BODY_SIZE_BYTES: int = 2_097_152
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 120
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    AUTH_RATE_LIMIT_ATTEMPTS: int = 5
    AUTH_RATE_LIMIT_WINDOW_SECONDS: int = 300

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    @field_validator("DATABASE_URL")
    def validate_database_url(cls, value: str) -> str:
        if not isinstance(value, str) or not value:
            raise ValueError("DATABASE_URL must be set.")

        valid_prefixes = (
            "sqlite://",
            "sqlite+pysqlite://",
            "postgresql://",
            "postgres://",
            "mysql://",
            "mysql+pymysql://",
        )

        if not value.startswith(valid_prefixes):
            raise ValueError("DATABASE_URL must be a valid SQLAlchemy database URL.")

        return value

    @field_validator("REDIS_URL")
    def validate_redis_url(cls, value: str) -> str:
        if not isinstance(value, str) or not value:
            raise ValueError("REDIS_URL must be set.")

        if not value.startswith(("redis://", "rediss://")):
            raise ValueError("REDIS_URL must use redis:// or rediss:// scheme.")

        return value

    @field_validator("SECRET_KEY")
    def validate_secret_key(
        cls,
        value: str,
        info: ValidationInfo,
    ) -> str:
        if not isinstance(value, str) or not value:
            raise ValueError("SECRET_KEY must be set.")

        debug = info.data.get("DEBUG", True)
        if not debug and len(value) < 32:
            raise ValueError("SECRET_KEY must be set and at least 32 characters long.")

        return value

    @field_validator("JWT_ALGORITHM")
    def validate_jwt_algorithm(cls, value: str) -> str:
        supported = {"HS256", "HS384", "HS512", "RS256", "ES256"}
        if value not in supported:
            raise ValueError(
                f"JWT_ALGORITHM must be one of: {', '.join(sorted(supported))}."
            )

        return value

    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES")
    def validate_access_token_ttl(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be greater than 0.")

        return value


settings = Settings()
