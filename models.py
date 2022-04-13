from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
import logging

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    username = Column(String, unique=True)
    password = Column(String(255))

