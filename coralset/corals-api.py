from fastapi import FastAPI, Path, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from database_utils import CoralDatabase, DB_FILENAME
from database import get_coral_by_catalog_number_db, get_coral_by_category_db, add_coral_to_db, update_coral_db, delete_coral_db
from api_utils import api_reply

app = FastAPI()
db = CoralDatabase()

class Coral(BaseModel):
    catalog_number: int
    data_provider: str
    scientific_name: str
    vernacular_name_category: str
    taxon_rank: str
    station: str
    observation_date: str
    latitude: str
    longitude: str
    depth: int

@app.get("/")
def root():
    return JSONResponse({'message': "Welcome to Corals-API"},
                        status_code=HTTP_200_OK)

@app.get("/coral/{catalog_number}")
def get_coral_by_catalog_number(catalog_number: int = Path(..., description="Catalog Number of the coral to retrieve")):
    coral = get_coral_by_catalog_number_db(catalog_number)
    return api_reply(coral)

@app.get("/coral-category/{coral_category}")
def get_coral_by_category(coral_category: str = Path(..., description="Category of corals you want to retrieve")):
    corals = get_coral_by_category_db(coral_category)
    return api_reply(corals)

@app.post("/new-coral/{catalog_number}")
def create_coral(catalog_number: int, coral: Coral):
    if get_coral_by_catalog_number_db(catalog_number):
        return JSONResponse({'message': 'Catalog Number Already Exists'},
                            status_code=HTTP_409_CONFLICT)
    add_coral_to_db(catalog_number,
                    coral.data_provider,
                    coral.scientific_name,
                    coral.vernacular_name_category,
                    coral.taxon_rank,
                    coral.station,
                    coral.observation_date,
                    coral.latitude,
                    coral.longitude,
                    coral.depth)
    return JSONResponse({'message': 'Coral Created Successfully'},
                        status_code=status.HTTP_201_CREATED)

@app.put("/update-coral/{catalog_number}")
def update_coral(catalog_number: str, coral: Coral):
    if not get_coral_by_catalog_number_db(catalog_number):
        return JSONResponse({'message': 'Coral Not Found'},
                            status_code=HTTP_404_NOT_FOUND)
    update_coral_db(catalog_number,
                coral.data_provider,
                coral.scientific_name,
                coral.vernacular_name_category,
                coral.taxon_rank,
                coral.station,
                coral.observation_date,
                coral.latitude,
                coral.longitude,
                coral.depth)
    return JSONResponse({'message': 'Coral Information Updated'},
                        status_code=status.HTTP_200_OK)

@app.delete("/delete-coral/{catalog_number}")
def delete_coral(catalog_number: str):
    if not get_coral_by_catalog_number_db(catalog_number):
        return JSONResponse({'message': 'Coral Not Found'},
                            status_code=HTTP_404_NOT_FOUND)
    delete_coral_db(catalog_number)
    return JSONResponse({'message': 'Coral Deleted Successfully'},
                        status_code=status.HTTP_200_OK)