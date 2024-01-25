import asyncio
from pathlib import Path

from aiohttp import web

from src.api.cities import router
from src.config import Config
from src.utils.utils import setup_initial_data

app = web.Application()


def run_app(port: int = 8000):
    if Config.CITIES_API_TOKEN == "":
        raise ValueError("No API token provided. Please provide an API token to Config class.")

    app.add_routes(router)

    web.run_app(app, port=port)


if __name__ == "__main__":
    asyncio.run(setup_initial_data(Path(__file__).parent.parent / "cities.csv"))
    run_app()
