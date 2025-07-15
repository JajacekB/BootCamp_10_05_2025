from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, declarative_base, relationship


engine = create_engine("sqlite:///fleet.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


