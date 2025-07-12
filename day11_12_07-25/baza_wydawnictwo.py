from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# DATABASE_URI = "sqlite:///publishers.db"
DATABASE_URI = "postgresql://myuser:mypassword@localhost/mydatabase"
Base = declarative_base()


# Author, Book, Publisher

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship("Book", back_populates='author')


class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship("Book", back_populates='publisher')


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)

    author_id = Column(Integer, ForeignKey('authors.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))

    author = relationship("Author", back_populates='books')
    publisher = relationship("Publisher", back_populates='books')


engine = create_engine(DATABASE_URI)

# utworzenie tabel
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# new_author = Author(name="Adam Mickieicz")
# new_publisher = Publisher(name="Wydawnictwo XYZ")
# new_book = Book(title="Pan Tadeusz", author=new_author, publisher=new_publisher)
#
# session.add_all(
#     [new_author, new_publisher, new_book]
# )

# new_author = Author(name="Jan Kowalski")
# new_publisher = Publisher(name="Wydawnictwo i Spółka")
# new_book = Book(title="Python Średniowiecze", author=new_author, publisher=new_publisher)

# session.add_all(
#     [new_author, new_publisher, new_book]
# )

session.commit()

# dodac jescze jednego autora, książkę, wydawnictwo
# odczytac z bazy autorów
# wypisać ksiazki autoró∑
# wypisac autor, ksiązka wydawnictwo
session.close()

authors = session.query(Author).all()
print(authors)
for author in authors:
    print(f"Author: {author.name}")
    for book in author.books:
        print(f"Książka: {book.title}, Wydawca: {book.publisher.name}")

print(111 * "-")

publishers = session.query(Publisher).all()
for publisher in publishers:
    print(f"Wydawca: {publisher.name}")
    for book in publisher.books:
        print(f"Książka: {book.title}")


