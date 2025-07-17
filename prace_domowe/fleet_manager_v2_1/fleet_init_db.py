# from fleet_models_db import *
# from fleet_database import Session, engine
# from sqlalchemy.exc import IntegrityError
# import bcrypt
#
# # Tworzenie tabel w bazie danych
# Base.metadata.create_all(engine)
# print("Baza danych i tabele zostały utworzone.")
#
# session = Session()
#
# # tworzenie konta Admin
# existing_admin = session.query(User).filter_by(login="admin").first()
#
# if not existing_admin:
#     admin_user = User(
#         first_name="Admin",
#         last_name="",
#         login="admin",
#         phone=666555444,
#         email="admin@system.local",
#         password_hash=bcrypt.hashpw("admin".encode(), bcrypt.gensalt()).decode(),
#         role="admin",
#         address=""
#     )
#     try:
#         session.add(admin_user)
#         session.commit()
#         print("Użytkownik 'admin' został utworzony")
#     except IntegrityError:
#         session.rollback()
#         print("Nie udało się utworzyć domyślnego admina (prawdopodobnie już istnieje).")
# else:
#     print("Urzytkownik 'admin' już istnieje.")
#
# session.close()