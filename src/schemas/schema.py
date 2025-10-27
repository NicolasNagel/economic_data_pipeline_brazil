from pydantic import BaseModel, field_validator
from datetime import datetime

class InflactionSchema(BaseModel):
    data: datetime
    valor: float

    @field_validator('data', mode='before')
    def parse_data(cls, v):
        return datetime.strptime(v, '%d/%m/%Y').date()
    
    @field_validator('valor', mode='before')
    def parse_valor(cls, v):
        try:
            return float(v.replace(',', '.'))
        except:
            return None