from pathlib import Path
import sqlite3
import pandas as pd

DB_FILENAME = "corals_db.db"
COLUMNS = ['catalog_number', 'data_provider', 'scientific_name',
        'vernacular_name_category', 'taxon_rank', 'station', 'observation_date',
        'latitude', 'longitude', 'depth']

def init_db(filename: str = DB_FILENAME) -> None:
    if not Path(filename).is_file():
        Path(filename).touch()
        
def load_csv_to_db() -> None:
    init_db(DB_FILENAME)
    conn = sqlite3.connect(DB_FILENAME)
    corals_data = pd.read_csv(r"C:\\Users\\anshu\\projects\\nextstag3\\FastAPI\\deep_sea_corals.csv")
    corals_data.drop(['DepthMethod', 'Locality', 'LocationAccuracy', 'SurveyID',
                      'Repository', 'IdentificationQualifier', 'EventID',
                      'SamplingEquipment', 'RecordType', 'SampleID'], axis=1, inplace=True)
                    
    corals_data.columns = COLUMNS
    try:
        corals_data.to_sql('Corals', conn, if_exists='fail', index=False)
    except ValueError:
        print("Table already exists")

def is_table_exists() -> bool:
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Corals'
    ''')
    
    return cursor.fetchone()[0]

class CoralDatabase:
    def __init__(self, file=DB_FILENAME):
        self.file = file
        if not is_table_exists():
            load_csv_to_db()
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()