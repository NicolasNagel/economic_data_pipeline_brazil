from src.data.data import data
from src.controllers.controller import get_data, transform_data, save_into_db

for item in data:
    url = item.get('URL')
    schema = item.get('schema')
    table = item.get('table')

    if not url or not schema or not table:
        print(f"Pular item: {item}")
        continue

    data = get_data(url, schema)
    df = transform_data(data)
    save_into_db(df, table)