from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


DATABASE_URI = 'mysql+pymysql://root:abc123@localhost:3306/zaawansowana_baza'

engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

