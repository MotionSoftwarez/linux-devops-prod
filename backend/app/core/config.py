from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Linux for DevOps"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "sqlite:///./linotutor.db"

    secret_key: str = "dev-secret-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    guest_mode_enabled: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
