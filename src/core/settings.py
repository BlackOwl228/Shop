from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    database_url: str

    test_database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/test"
    main_email: str = "example@gmail.com"
    google_client_id: str = "test_client_id"
    google_client_secret: str = "test_client_secret"
    google_refresh_token: str = "test_refresh_token"
    stripe_secret_key: str = "test_stripe_secret_key"

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14
    verification_email_token_hours: int = 12
    rate_limit_per_minute: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # 🔥 ВОТ ЭТО
    )


settings = Settings()
