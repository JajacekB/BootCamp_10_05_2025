from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DATABASE_URI = "sqlite:///parents_database.db"

engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    children = relationship("Child", backref="parent")
    # parents =  [{"id":1, "name": "Radek", "children": []}]


class Child(Base):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    parent_id = Column(Integer, ForeignKey('parents.id'))

    def __repr__(self):
        return f"id={self.id}, name={self.name}"


Base.metadata.create_all(engine)

Sesion = sessionmaker(bind=engine)
session =Sesion()

# parent = Parent(name="Rodzic")
# child1 = Child(name="Dziecko 1", parent=parent)
# child2 = Child(name="Dziecko 2", parent=parent)
#
# session.add_all(
#     [parent, child1, child2]
# )


session.commit()

our_parent = session.query(Parent).all()
print(our_parent)

our_parent_filtered = session.query(Parent).filter_by(name="Rodzic").first()
print(f"Rodzic: {our_parent_filtered.name}")

children = our_parent_filtered.children
for child in children:
    print(f"Dziecko: {child.name}")
    print(f"Rodzic: {child.parent.name}")







