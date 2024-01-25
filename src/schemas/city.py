from pydantic import BaseModel, ConfigDict


class CityCreateSchema(BaseModel):
    name: str


class CityGetSchema(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float

    model_config = ConfigDict(from_attributes=True)


class CityWithDistanceGetSchema(CityGetSchema):
    distance: float = 0.0


class Coordinates(BaseModel):
    longitude: float
    latitude: float
