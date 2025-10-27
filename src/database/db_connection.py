from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_CONNECTION = 'sqlite:///mydatabase.db'

engine = create_engine(DB_CONNECTION)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
Base = declarative_base(engine)