import requests
import pandas as pd

from typing import List, Dict, Any

from src.schemas.schema import InflactionSchema
from src.database.db_model import InflactionTable
from src.database.db_connection import engine, Base, Session

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'

Base.metadata.create_all(bind=engine)

def get_data() -> List[Dict[Any, Any]]:
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        validated_data = [InflactionSchema(**item).model_dump() for item in data]
        return validated_data
    else:
        print(f"Erro ao se conectar com a API BACEN.")


def transform_data(data: tuple) -> pd.DataFrame:
    if not data:
        print('Nenhum registro encontrado.')
        return None
    
    df = pd.DataFrame(data)

    return df
    

def save_into_db(df: pd.DataFrame) -> InflactionTable:
    if df.empty:
        print('Nenhum registro encontrado no DataFrame.')
        return None
    
    with Session() as session:
        registros = [
            InflactionTable(**row._asdict())
            for row in df.itertuples(index=False)
        ]
        session.add_all(registros)
        session.commit()

    return print(f"{len(registros)} registros salvos no Banco de Dados.")