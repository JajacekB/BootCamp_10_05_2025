from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base, aliased

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return  f"<User(name={self.name}, ege={self.age}"


engine = create_engine('sqlite:///mydatabase.db', echo=True)
Base.metadata.create_all(engine)



Session = sessionmaker(bind=engine)
session = Session()

new_user = User(name="Iwonka Konopalska", age=23)
session.add(new_user)

session.commit()
session.close()

users = session.query(User).all()
for user in users:
    print(user)
    print(f"Imię: {user.name} wiek: {user.age}")

result = session.execute(text("SELECT * FROM users"))
for row in result:
    print(row)


stmt = text("SELECT * FROM users")
result = session.query(User).from_statement(stmt).all()

for user in users:
    print(type(user))
    print(user.name)