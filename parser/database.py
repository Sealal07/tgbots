from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/car_db'

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    cars = relationship('Car', back_populates='brand_rel', cascade='all, delete-orphan')


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(String)
    params = Column(String)
    link = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now())

    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand_rel = relationship('Brand', back_populates='cars')

def init_db():
    Base.metadata.create_all(bind=engine)

