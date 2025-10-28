import requests
import pandas as pd

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.sql import func
from typing import List, Dict, Any, Tuple, AnyStr
from datetime import datetime, timedelta

from src.database.db_connection import engine, Base, Session

Base.metadata.create_all(bind=engine)

def get_data(url: str, schema, start_date: str = None, end_date: str = None) -> List[Dict[AnyStr, Any]]:
    """
    Baixa os dados da API em janelas de 10 anos e valida com Pydantic.

    Args:
        url (str): URL base da API.
        schema: classe Pydantic para validação.
        start_date (str): data inicial da extração.
        end_date (str): data final da extração.

    Returns:
        List[Dict]: Lista com todos os registros validados
    """
    all_data: list = []

    if start_date and end_date:
        intervals = generate_interval(start_date, end_date)
    else:
        intervals = [(None, None)]

    for start, end in intervals:
        if start and end:
            full_url = f"{url}&dataInicial={start}&dataFinal={end}"
        else:
            full_url = url

        print(f"  📡 Consultando: {full_url}")

        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                validated_data = [schema(**item).model_dump() for item in data]
                all_data.extend(validated_data)
                print(f"  ✓ {len(validated_data)} registros baixados")
            else:
                print(f"  ⚠️ Status {response.status_code} para intervalo {start} - {end}")
                
        except Exception as e:
            print(f"  ❌ Erro ao processar dados de {full_url}: {e}")

    if not all_data:
        print("  ⚠️ Nenhum dado foi retornado da API.")
    
    return all_data



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
        return pd.DataFrame()
    
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
    if df is None or df.empty:
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


def get_min_and_max_date(tables: list, date_column: str ='data'):
    """
    Calcula a data mínima e máxima considerando todas as tabelas.

    Args:
        tables (list): Lista de classes ORM SQLAlchemy.
        date_column (str): Nome da coluna de data em todas as tabelas.

    Returns:
        tuple: (global_min_date, global_max_date) no formato 'dd/mm/yyyy'
    """
    if not isinstance(tables, (list, tuple)):
        tables = [tables]

    global_min = None
    global_max = None

    with Session() as session:
        for table in tables:
            min_date, max_date = session.query(
                func.min(getattr(table, date_column)),
                func.max(getattr(table, date_column))
            ).first()

            if min_date:
                if global_min is None or min_date < global_min:
                    global_min = min_date
            if max_date:
                if global_max is None or max_date > global_max:
                    global_max = max_date

        if global_min is None:
            global_min = datetime(1950, 1, 1)
        if global_max is None:
            global_max = datetime.now()

        return global_min.strftime('%d/%m/%Y'), global_max.strftime('%d/%m/%Y')
    

def generate_interval(start_date: str, end_date: str) -> List[Tuple[AnyStr]]:
    """
    Gera intervalos de até 10 anos para consulta na API do BACEN.

    Args:
        start_date (str): data inicial 'dd/mm/yyyy'
        end_date (str): data final 'dd/mm/yyyy'

    Returns:
        list: lista de tuplas (data_inicial, data_final)
    """
    start = datetime.strptime(start_date, '%d/%m/%Y')
    end = datetime.strptime(end_date, '%d/%m/%Y')
    intervals: list = []

    while start < end:
        interval_end = min(start + timedelta(days=360 * 10), end)
        intervals.append((start.strftime('%d/%m/%Y'), interval_end.strftime('%d/%m/%Y')))
        start = interval_end + timedelta(days=1)

    return intervals