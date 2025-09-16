from database_utils import CoralDatabase, DB_FILENAME
def get_coral_by_catalog_number_db(catalog_number: int) -> dict:
    with CoralDatabase(DB_FILENAME) as cursor:
        cursor.execute('''SELECT catalog_number, data_provider,
           scientific_name, vernacular_name_category, taxon_rank,
           observation_date, latitude, longitude, depth
           FROM Corals WHERE catalog_number = ?''',
                       (catalog_number,))
        return cursor.fetchone()

def get_coral_by_category_db(coral_category: str) -> list:
    with CoralDatabase(DB_FILENAME) as cursor:
        cursor.execute('''SELECT catalog_number, data_provider,
           scientific_name, vernacular_name_category, taxon_rank,
           observation_date, latitude, longitude, depth
           FROM Corals WHERE vernacular_name_category = ?''',
                       (coral_category,))
        return cursor.fetchall()
    
def add_coral_to_db(catalog_number: int, data_provider: str, 
                    scientific_name: str, 
                    vernacular_name_category: str,
                    taxon_rank: str, station: str,   
                    observation_date: str, latitude: str,
                    longitude: str, depth: int) -> None:
    with CoralDatabase(DB_FILENAME) as cursor:
        cursor.execute('''
        INSERT INTO Corals ('catalog_number', 'data_provider', 'scientific_name',
        'vernacular_name_category', 'taxon_rank', 'station', 'observation_date',
        'latitude', 'longitude', 'depth') VALUES (?,?,?,?,?,?,?,?,?,?)''',
         (catalog_number, data_provider, scientific_name, vernacular_name_category,
          taxon_rank, station, observation_date, latitude, longitude, depth))
        
def update_coral_db(catalog_number_identifier: int, 
                    data_provider: str = None,
                    scientific_name: str = None,
                    vernacular_name_category: str = None,
                    taxon_rank: str = None,
                    station: str = None,
                    observation_date: str = None,
                    latitude: str = None, 
                    longitude: str = None,
                    depth: int = None) -> None:
    params = [data_provider, scientific_name,  
              vernacular_name_category, taxon_rank, station, 
              observation_date, latitude, longitude, depth]
    params_names = ['data_provider', 'scientific_name',
                    'vernacular_name_category', 'taxon_rank', 
                    'station', 'observation_date', 'latitude',
                    'longitude', 'depth']
    with CoralDatabase(DB_FILENAME) as cursor:
        for param, param_name in zip(params, params_names):
            if param and param != 'string':
                query = '''
                UPDATE Corals SET ''' + param_name + ''' = ? WHERE 
                catalog_number = ?'''
                cursor.execute(query, (param, 
                                catalog_number_identifier))
                

def delete_coral_db(catalog_number: int) -> None:
    with CoralDatabase(DB_FILENAME) as cursor:
        cursor.execute('''
        DELETE FROM Corals WHERE catalog_number = ?''', (catalog_number,))