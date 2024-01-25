from pathlib import Path


class Config:
    ROOT_DIR: Path = Path(__file__).parent.parent
    DB_NAME: str = "database.db"
    DB_PATH: Path = ROOT_DIR / DB_NAME
    DB_URL: str = f"sqlite+aiosqlite:///{DB_PATH}"

    CITIES_API_URL: str = f"https://api.api-ninjas.com/v1"
    CITIES_API_TOKEN: str = ""
