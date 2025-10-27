import requests
import pandas as pd

from typing import List, Dict, Any

from src.schemas.schema import InflactionSchema

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'

def get_data() -> List[Dict[Any, Any]]:
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        validated_data = [InflactionSchema(**item).model_dump() for item in data]
        return validated_data
    else:
        print(f"Erro ao se conectar com a API BACEN.")


def transform_data(data: tuple) -> pd.DataFrame:
    data = get_data()
    df = pd.DataFrame(data)
    if df.empty:
        return None
    else:
        return df