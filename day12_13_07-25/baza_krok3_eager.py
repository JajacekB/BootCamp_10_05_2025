from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from baza_krok1 import Users, Post
from baza_krok2_tranzakcja import Session

DATABASE_URI = 'mysql+pymysql://root:abc123@localhost:3306/zaawansowana_baza'

session  = Session()

# user_with_posts = session.query(Users).all()

# for user in user_with_posts:
#     print(f"Użtkownik: {user.name}")
#     for post in user.posts:
#         print(f"   Post:  {post.title}")


users_with_posts = session.query(Users).options(joinedload(Users.posts)).all()
for user in users_with_posts:
    print(f"Użtkownik: {user.name}")
    for post in user.posts:
        print(f"   Post:  {post.title}")

