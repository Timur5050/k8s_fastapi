from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Urls response check"

    DATABASE_URL: str | None = "sqlite:///./fastapik8s.sqlite3"
    ASYNC_DATABASE_URL: str | None = "sqlite+aiosqlite:///./fastapik8s.sqlite3"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
