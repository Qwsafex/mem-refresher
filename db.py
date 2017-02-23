import datetime
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Enum

# DB classes

engine = create_engine('sqlite:///mem-refresher.db')
Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    type = Column(Enum('SINGLE', 'MULTIPLE'))
    answer = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
