from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    # AI
    OPENROUTER_API_KEY: str
    OPENROUTER_AI_MODEL: str

    # DB
    DB_URL: str
    DB_POOL_SIZE: int
    DB_POOL_TIMEOUT: int
    DB_POOL_RECYCLE: int
    DB_POOL_PRE_PING: bool

    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
