from sqlalchemy import Column, Float, Integer, String
from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), index=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    price = Column(Float, nullable=False)
    