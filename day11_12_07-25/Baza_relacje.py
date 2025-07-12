from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DATABASE_URI = "sqlite:///adress_book.db"

engine = create_engine(DATABASE_URI, echo=False)
Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)

    addresses =relationship(
        'Address',
        back_populates='person',
        order_by='Address.email',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"{self.name} (id={self.id}"


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    person_id = Column(ForeignKey('person.id'))
    person = relationship("Person", back_populates='addresses')

    def __repr__(self):
        return self.email

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

anakin = Person(name='Anakin', age=38)

anakin1 = Person(name='Anaki Anakin', age=38)
anakin1.addresses = [Address(email='anakin@wp.pl')]

obi_wan = Person(name='Obi Wan', age=39)
obi_wan.addresses = [
    Address(email='obiwan@op.pl'),
    Address(email='obiwan@wp.pl')
]

chewee = Person(name="CHewbacca", age=190)
chewee.addresses = [
    Address(email='chewbacca@op.pl'),
    Address(email='chewee@wp.pl')
]

session.add(anakin)
session.add(anakin1)
session.add(obi_wan)
session.add(chewee)

session.commit()

all_ = session.query(Person).all()
print(all_)
print(type(all_))


first = session.query(Person).first()
print(first)
print(type(first))
print(first.name, first.age)

obi_list = session.query(Person).filter(
    Person.name.like('Obi%')
).all()

print(obi_list)


chewee_list = session.query(Person).filter(
    Person.name.like('CHe%')
).all()

print(chewee_list)

for chewee in chewee_list:
    print(f"{chewee.id=}, {chewee.name=}, {chewee.addresses=}")
