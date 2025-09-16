from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
def prepare_result(data):
    if not isinstance(data, list):
        data = [data]
        
    result = {}
    for idx, entry in enumerate(data):
        result[idx] = {"CatalogNumber": entry[0],
                       "DataProvider": entry[1],
                       "ScientificName": entry[2],
                       "VernacularNameCategory": entry[3],
                       "TaxonRank": entry[4],
                       "ObservationDate": entry[5],
                       "Latitude": entry[6],
                       "Longitude": entry[7],
                       "Depth": entry[8]
                       }
    return result

def api_reply(data):
    if not data:
        return JSONResponse({'message': 'Coral Not Found'},
                            status_code=HTTP_404_NOT_FOUND)
    result = prepare_result(data)
    return JSONResponse({'message': 'Coral Found',
                         'data': result}, status_code=HTTP_200_OK)

