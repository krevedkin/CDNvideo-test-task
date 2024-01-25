import csv

from sqlalchemy.exc import IntegrityError

from src.db.db import async_session_maker
from src.models.city import CityModel


async def setup_initial_data(csv_file_path=None):
    with open(csv_file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)

        cities = []
        for row in csv_reader:
            cities.append(CityModel(name=row[0], longitude=float(row[1]), latitude=float(row[2])))

        async with async_session_maker() as session:
            session.add_all(cities)
            print("Add initial data in database")
            try:
                await session.commit()
            except IntegrityError:
                print("Initial data already added")
