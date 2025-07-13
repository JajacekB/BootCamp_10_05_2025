import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, select


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)


engin = create_async_engine("sqlite+aiosqlite:///async.db", echo=True)
Session = async_sessionmaker(engin, expire_on_commit=False)

async def main():
    async with engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async  with Session() as session:
        session.add_all([User(name="Ala"), User(name="Ola")])
        await session.commit()

        result = await session.execute(select(User))
        for user in result.scalars():
            print(f"[ASYNC] Użytkownik: {user.name}")


if __name__ == '__main__':
    asyncio.run(main())