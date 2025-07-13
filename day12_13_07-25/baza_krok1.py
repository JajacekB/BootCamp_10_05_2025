from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


DATABASE_URI = 'mysql+pymysql://root:abc123@localhost:3306/zaawansowana_baza'

engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)

    posts = relationship("Post", back_populates='user')


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("Users", back_populates='posts')


Base.metadata.create_all(engine)


