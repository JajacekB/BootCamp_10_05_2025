from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from baza_krok1 import Users, Post


DATABASE_URI = 'mysql+pymysql://root:abc123@localhost:3306/zaawansowana_baza'

engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

try:

    new_user = Users(name="Jan Kowalski", email='jan.kowalski@wp.pl')
    session.add(new_user)

    new_user = Post(title="Pierwszy post", content='To jest treść pierwszego posta.', user=new_user)
    session.add(new_user)

    session.commit()
except Exception as e:
    print("Błąd:", e)
    session.rollback()

finally:
    session.close()