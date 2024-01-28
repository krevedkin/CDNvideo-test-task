from geopy import Point, distance

from src.client.http_client import HttpClient
from src.dao.city_dao import CityDao
from src.models import CityModel
from src.schemas.city import CityCreateSchema, CityGetSchema, CityWithDistanceGetSchema


class CoordinatesError(Exception):
    ...


class CityNotFoundError(Exception):
    ...


class CityManager:
    @staticmethod
    async def create_city(city: CityCreateSchema) -> None:
        coordinates = await HttpClient.get_coords_data(city.name)
        await CityDao.create(**city.model_dump(), **coordinates.model_dump())

    @staticmethod
    async def delete_city(name: str) -> CityModel | None:
        return await CityDao.delete(name=name)

    @staticmethod
    async def get_city(name: str) -> CityGetSchema | None:
        city = await CityDao.get(name=name.capitalize())

        if not city:
            raise CityNotFoundError("Not found")

        return CityGetSchema.model_validate(city)

    @staticmethod
    async def get_all_cities() -> list[CityGetSchema]:
        cities = await CityDao.get_all()
        return [CityGetSchema.model_validate(city) for city in cities]

    @staticmethod
    async def get_nearest_cities_to_coordinates(longitude: float, latitude: float) -> list[CityWithDistanceGetSchema]:
        try:
            coordinates = Point(latitude=latitude, longitude=longitude)

            cities_with_distance = [
                CityWithDistanceGetSchema(
                    id=city.id,
                    name=city.name,
                    longitude=city.longitude,
                    latitude=city.latitude,
                    distance=distance.distance(
                        coordinates,
                        Point(city.latitude, city.longitude),
                    ).kilometers,
                )
                for city in await CityDao.get_all()
            ]

            sorted_cities = sorted(cities_with_distance, key=lambda x: x.distance)
        except ValueError:
            raise CoordinatesError("Latitude must be in the [-90; 90] range.")

        if len(sorted_cities) == 1:
            return sorted_cities[:1]
        elif len(sorted_cities) >= 2:
            return sorted_cities[:2]

        return []
