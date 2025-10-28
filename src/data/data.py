from src.schemas.schema import InflactionSchema, SelicSchema
from src.database.db_model import InflactionTable, SelicTable

data = [
    {
        'URL': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json',
        'schema': InflactionSchema,
        'table': InflactionTable,
        'unique_keys': ['data'],
    },
    {
        'URL': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.21864/dados?formato=json',
        'schema': SelicSchema,
        'table': SelicTable,
        'unique_keys': ['data'],
    },
]