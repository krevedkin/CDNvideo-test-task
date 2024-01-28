from json.decoder import JSONDecodeError

from aiohttp.web import Request, Response, RouteTableDef, json_response
from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPConflict,
    HTTPInternalServerError,
    HTTPNotFound,
    HTTPUnprocessableEntity,
)
from pydantic import ValidationError

from src.client.http_client import HttpClientCoordsForCityNotFoundError, HttpClientError
from src.dao.base import RecordAlreadyExistsError
from src.managers.city_manager import CityManager, CityNotFoundError, CoordinatesError
from src.schemas.city import CityCreateSchema

router = RouteTableDef()


@router.get("/cities")
async def get_cities(request: Request) -> Response:
    cities = await CityManager.get_all_cities()

    return json_response([city.model_dump() for city in cities])


@router.get("/city/{name}")
async def get_city(request: Request) -> Response:
    name = request.match_info.get("name")

    if not name:
        raise HTTPBadRequest(reason="name required")

    try:
        city = await CityManager.get_city(name)
    except CityNotFoundError as e:
        raise HTTPNotFound(reason=e.args[0])

    return json_response(city.model_dump())


@router.post("/city")
async def add_city(request: Request) -> Response:
    try:
        data = await request.json()
        data["name"] = data["name"].capitalize() if data.get("name") else None
        await CityManager.create_city(CityCreateSchema(**data))
    except JSONDecodeError:
        raise HTTPBadRequest(reason="provide valid json")
    except ValidationError:
        raise HTTPUnprocessableEntity(reason="Validation error")
    except RecordAlreadyExistsError:
        raise HTTPConflict(reason="City already added")
    except HttpClientCoordsForCityNotFoundError as e:
        raise HTTPBadRequest(reason=e.args[0])
    except HttpClientError as e:
        raise HTTPInternalServerError(reason=e.args[0])

    return json_response({"ok": True}, status=201)


@router.delete("/city/{name}")
async def delete_city(request: Request) -> Response:
    name = request.match_info.get("name")

    if not name:
        raise HTTPBadRequest(reason="name required")
    deleted_city = await CityManager.delete_city(name=name)

    if not deleted_city:
        raise HTTPNotFound(reason="City not found")

    return json_response(status=204)


@router.get("/cities/nearest")
async def get_nearest_cities_by_coordinates(request: Request) -> Response:
    longitude = request.query.get("longitude")
    latitude = request.query.get("latitude")

    if not longitude or not latitude:
        raise HTTPBadRequest(reason="Provide longitude and latitude")

    try:
        longitude, latitude = float(longitude), float(latitude)
        cities = await CityManager.get_nearest_cities_to_coordinates(longitude, latitude)
    except ValueError:
        raise HTTPUnprocessableEntity(reason="longitude and latitude must be digit")
    except CoordinatesError as e:
        raise HTTPUnprocessableEntity(reason=e.args[0])

    return json_response([city.model_dump() for city in cities])
