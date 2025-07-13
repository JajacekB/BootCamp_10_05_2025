from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)


engine = create_engine("sqlite:///sync.db", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([User(name="Ala"), User(name="Ola")])
    session.commit()

    result = session.execute(select(User))
    for user in result.scalars():
        print(f"[SYNC] Uzytkownik: {user.name}")

