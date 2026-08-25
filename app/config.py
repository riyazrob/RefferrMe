from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Reffery"
    secret_key: str = "change-me-in-production"
    database_url: str = "sqlite:///./reffery.db"
    debug: bool = True

    # Optional SMTP settings for outgoing email
    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None
    smtp_tls: bool = True


settings = Settings()
