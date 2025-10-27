from src.controllers.controller import get_data, transform_data, save_into_db

data = get_data()
df = transform_data(data)
save_into_db(df)