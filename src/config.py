from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ROOT_DIR: Path = Path(__file__).parent.parent
    DB_NAME: str = "database.db"
    DB_PATH: Path = ROOT_DIR / DB_NAME
    DB_URL: str = f"sqlite+aiosqlite:///{DB_PATH}"

    CITIES_API_URL: str = "https://api.api-ninjas.com/v1"
    CITIES_API_TOKEN: str


config = Config()
