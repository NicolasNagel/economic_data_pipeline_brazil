from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.sql import func

from src.database.db_connection import Base

class InflactionTable(Base):
    __tablename__ = 'raw_inflaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, nullable=False)
    valor = Column(Float, nullable=False)
    dt_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())


class SelicTable(Base):
    __tablename__ = 'raw_selic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, nullable=False)
    valor = Column(Float, nullable=False)
    dt_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())