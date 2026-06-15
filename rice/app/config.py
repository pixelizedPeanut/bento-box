from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    CORS_ORIGINS: list[str]
    MAX_BOOKINGS: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# We use type: ignore because static type checkers flag empty initialization here,
# unaware that pydantic-settings populates these arguments from the env at runtime.
settings = Settings()  # type: ignore
