

# users = session.query(User).filter(User.role != "admin").all()
# for user in users:
#     print(user)


# def delete_user():
#     login_to_delete = input("Podaj login użytkownika do usunięcia: ").strip()
#     user = session.query(User).filter_by(login=login_to_delete).first()
#
#     if not user:
#         print("Nie znaleziono użytkownika.")
#         return
#
#     if user.role == "admin":
#         print("Nie można usunąć konta administratora systemowego.")
#         return
#
#     session.delete(user)
#     session.commit()
#     print(f"Użytkownik {login_to_delete} został usunięty.")