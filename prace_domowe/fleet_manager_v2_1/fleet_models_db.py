from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from prace_domowe.fleet_manager_v2_1.fleet_database import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(String, unique=True, nullable=False)
    brand = Column(String, nullable=False)
    vehicle_model = Column(String, nullable=False)
    cash_per_day = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    borrower = Column(String, nullable=True)
    return_date = Column(Date, nullable=True)
    type = Column(String)  # 'car', 'scooter', 'bike'

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'vehicle'
    }


class Car(Vehicle):
    __tablename__ = 'cars'
    id = Column(Integer, ForeignKey('vehicles.id'), primary_key=True)  # <-- klucz obcy do vehicles.id
    size = Column(String)
    fuel_type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'car',
    }

    def __repr__(self):
        return(
            f"<Car {self.vehicle_id}\n"
            f"{self.brand}, {self.vehicle_model}\n"
            f"{self.size}, {self.fuel_type}>"
        )


class Scooter(Vehicle):
    __tablename__ = 'scooters'
    id = Column(Integer, ForeignKey('vehicles.id'), primary_key=True)
    max_speed = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'scooter',
    }

    def __repr__(self):
        return (
            f"<Scooter {self.vehicle_id}\n"
            f"{self.brand}, {self.vehicle_model}\n"
            f"{self.max_speed}km/h>"
        )


class Bike(Vehicle):
    __tablename__ = 'bikes'
    id = Column(Integer, ForeignKey('vehicles.id'), primary_key=True)
    bike_type = Column(String)
    is_electric = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'bike',
    }

    def __repr__(self):
        return (
            f"<Bike {self.vehicle_id}\n"
            f"{self.brand}, {self.vehicle_model}\n"
            f"{self.bike_type}, {'elektryczny' if self.is_electric else 'zwykły'}>"
        )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)  # 'admin', 'seller', 'client'
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    address = Column(String, nullable=True)

    def __repr__(self):
        return f"<User {self.login} ({self.role})>"