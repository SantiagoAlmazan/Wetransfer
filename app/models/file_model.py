from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True)
    filename = Column(String)
    token = Column(String, unique=True)
    expires_at = Column(DateTime)