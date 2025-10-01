# directory: models
# file: user.py

from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import date
from database import Base



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    address = Column(String, nullable=True)
    registration_day = Column(Date, default=date.today)
    is_active = Column(Boolean, nullable=False, default=True)

    vehicles = relationship("Vehicle", back_populates="borrower")
    rental_history = relationship("RentalHistory", back_populates="user")
    repairs_done = relationship("RepairHistory", back_populates="mechanic", foreign_keys="RepairHistory.mechanic_id")

    def __repr__(self):
        return (
            f"\n[ID={self.id}]\n"
            f"{self.first_name} {self.last_name}\n"
            f"Login: {self.login}\n"
            f"zamieszkały: {self.address}\n"
            f"Telefon: {self.phone} email: {self.email}\n"
        )