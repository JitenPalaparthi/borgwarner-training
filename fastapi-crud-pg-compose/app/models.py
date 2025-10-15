from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True, index=True)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False, default=0.0)
