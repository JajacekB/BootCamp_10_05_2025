

if isinstance(user, Admin):
    admin_menu()
elif isinstance(user, Seller):
    seller_menu()
elif isinstance(user, Client):
    client_menu()