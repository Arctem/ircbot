from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = None
session = None

def initialize(dbname='sqlite:///:memory:'):
  global engine, session
  engine = create_engine(dbname, echo=True)
  session = sessionmaker(bind=engine)
  Base.metadata.create_all(engine)



