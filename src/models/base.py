from datetime import datetime

from sqlalchemy import Column, Integer, DateTime,JSON
from sqlalchemy.sql import func

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

metadata = Base.metadata

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True,autoincrement=True)
    created_at  = Column(DateTime, server_default= func.now())
    updated_at  = Column(DateTime, server_default= func.now(), onupdate=func.now())
