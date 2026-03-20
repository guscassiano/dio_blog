from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )

    database_url: str
    environment: str = "production"
    email_username: str
    email_password: str
    email_from: str
    email_port: int = 465
    email_server: str = "smtp.gmail.com"
    email_starttls: bool = False
    email_ssl_tls: bool = True


settings = Settings()
