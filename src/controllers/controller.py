import requests
import pandas as pd

from sqlalchemy.dialects.sqlite import insert
from typing import List, Dict, Any

from src.database.db_connection import engine, Base, Session

Base.metadata.create_all(bind=engine)

def get_data(url: str, schema) -> List[Dict[Any, Any]]:
    """
    Faz a requisição de dados de uma API e valida os registros usando Pydantic.

    Args:
        url (str): Endpoint da API de onde os dados serão extraídos.
        schema (BaseModel): Classe Pydantic usada para validação de cada item da resposta.

    Returns:
        List[Dict[Any, Any]]: Lista de dicionários com os dados validados. 
        Retorna None se houver erro na requisição.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        validated_data = [schema(**item).model_dump() for item in data]
        return validated_data
    else:
        print(f"Erro ao se conectar com a API BACEN.")


def transform_data(data: tuple) -> pd.DataFrame:
    """
    Transforma uma lista de dicionários em um DataFrame do Pandas.

    Args:
        data (tuple): Lista de dicionários contendo os dados validados.

    Returns:
        pd.DataFrame: DataFrame contendo os dados.
        Retorna None se a lista estiver vazia ou nula.
    """
    if not data:
        print('Nenhum registro encontrado.')
        return None
    
    df = pd.DataFrame(data)

    return df
    

def save_into_db(df: pd.DataFrame, table, unique_keys: list) -> None:
    """
    Salva ou atualiza registros no banco de dados de forma incremental (upsert).

    Para cada registro no DataFrame, insere um novo registro se a chave única
    não existir, ou atualiza os campos caso já exista.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem salvos.
        table (DeclarativeMeta): Classe ORM SQLAlchemy da tabela de destino.
        unique_keys (list): Lista de colunas que definem a unicidade do registro 
                            para aplicar o upsert.

    Returns:
        None: Apenas imprime a quantidade de registros inseridos/atualizados.
    """
    if df.empty:
        print('Nenhum registro encontrado no DataFrame.')
        return None
    
    with Session() as session:
        for row in df.itertuples(index=False):
            row_dict = row._asdict()

            stmt = insert(table).values(**row_dict)
            update_dict = {col: row_dict[col] for col in row_dict if col not in unique_keys}
            stmt = stmt.on_conflict_do_update(
                index_elements=unique_keys,
                set_ = update_dict
            )

            session.execute(stmt)

        session.commit()

    return print(f"{len(df)} registros salvos/atualizados no Banco de Dados.")