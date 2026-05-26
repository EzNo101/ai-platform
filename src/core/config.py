from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    # AI
    OPENROUTER_API_KEY: str
    OPENROUTER_AI_MODEL: str

    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
