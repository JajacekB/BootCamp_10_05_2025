# directory: database
# file: base.py

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL, DEBUG

# engine = create_engine(
#     DATABASE_URL,
#     echo=DEBUG,
#     connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
# )
engine = create_engine(
    DATABASE_URL,
    echo=DEBUG,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

# Session = sessionmaker(bind=engine, expire_on_commit=False)
# from models.user import User
# from models.vehicle import Vehicle, Car, Bike, Scooter
# from models.repair_history import RepairHistory
# from models.rental_history import RentalHistory
# from models.promotions import Promotion
# from models.invoice import Invoice