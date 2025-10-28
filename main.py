from src.data.data import data
from src.controllers.controller import get_data, transform_data, save_into_db, get_min_and_max_date

for item in data:
    url = item.get('URL')
    schema = item.get('schema')
    table = item.get('table')
    unique_keys = item.get('unique_keys')
    contains_filter = item.get('contains_filter', False)

    if not url or not schema or not table:
        print(f"Pular item: {item}")
        continue

    all_tables = [item['table'] for item in data]
    start_date, end_date = get_min_and_max_date(all_tables)

    if contains_filter:
        api_data = get_data(url, schema,start_date=start_date, end_date=end_date)
    else:
        api_data = get_data(url, schema)

    df = transform_data(api_data)
    save_into_db(df, table, unique_keys)