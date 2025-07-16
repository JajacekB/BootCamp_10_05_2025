from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


engine = create_engine("sqlite:///fleet.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False)


