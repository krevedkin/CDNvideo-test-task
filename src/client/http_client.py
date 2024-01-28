import aiohttp

from src.config import config
from src.schemas.city import Coordinates


class HttpClientError(Exception):
    ...


class HttpClientCoordsForCityNotFoundError(Exception):
    ...


class HttpClient:
    @staticmethod
    async def get_coords_data(city_name: str) -> Coordinates:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                config.CITIES_API_URL + f"/city?name={city_name}", headers={"X-Api-Key": config.CITIES_API_TOKEN}
            ) as resp:
                if not resp.ok:
                    raise HttpClientError(
                        "Failed to get coordinates from external API service. Please ensure your API key is valid."
                    )

                if resp.status == 200:
                    data = await resp.json()

                    if not data:
                        raise HttpClientCoordsForCityNotFoundError("Provide correct city name")

                    data = data[0]

                    return Coordinates(latitude=data["latitude"], longitude=data["longitude"])
                else:
                    raise HttpClientError("Can't get coordinates for city " + city_name)
