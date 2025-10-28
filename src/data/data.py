from src.schemas.schema import InflactionSchema, SelicSchema, IGPDISchema, CDISchema, PIBSchema, CambioSchema
from src.database.db_model import InflactionTable, SelicTable, IGPDITable, CDITable, PIBTable, CambioTable

data = [
    {
        'URL': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json',
        'schema': InflactionSchema,
        'table': InflactionTable,
        'unique_keys': ['data'],
        'contains_filter': False,
    },
    {
        'URL': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.21864/dados?formato=json',
        'schema': SelicSchema,
        'table': SelicTable,
        'unique_keys': ['data'],
        'contains_filter': False
    },
    {
        'URL': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json',
        'schema': IGPDISchema,
        'table': IGPDITable,
        'unique_keys': ['data'],
        'contains_filter': True
    },
    {
        'URL': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados?formato=json',
        'schema': CDISchema,
        'table': CDITable,
        'unique_keys': ['data'],
        'contains_filter': True
    },
    {
        'URL': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4380/dados?formato=json',
        'schema': PIBSchema,
        'table': PIBTable,
        'unique_keys': ['data'],
        'contains_filter': True
    },
    {
        'URL': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json',
        'schema': CambioSchema,
        'table': CambioTable,
        'unique_keys': ['data'],
        'contains_filter': True
    },
]