from src.dao.base import BaseDao
from src.models.city import CityModel


class CityDao(BaseDao):
    model = CityModel
