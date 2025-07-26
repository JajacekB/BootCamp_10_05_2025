def _rent_vehicle_for_admin_seller(user, vehicle_id, client_id=None):
    if client_id is None:
        # wypożycza dla siebie z rabatem
        print(f"{user.role} {user.name} wypożycza dla siebie z rabatem.")
    else:
        # wypożycza dla klienta
        print(f"{user.role} {user.name} wypożycza dla klienta {client_id}.")
    # dalsza logika


def _rent_vehicle_for_client(user, vehicle_id):
    # klient może wypożyczać tylko dla siebie, bez rabatu
    print(f"Klient {user.name} wypożycza pojazd {vehicle_id}.")


def rent_vehicle(user, vehicle_id, client_id=None):
    if user.role in ("Admin", "Seller"):
        return _rent_vehicle_for_admin_seller(user, vehicle_id, client_id)
    elif user.role == "Client":
        return _rent_vehicle_for_client(user, vehicle_id)
    else:
        print("Brak dostępu")_id}.")

        def _get_vehicle_for_admin_seller(user):
            # zwraca pełne info, wszystkie pojazdy
            print("Zwracam pojazdy z pełnym info dla admina/sellera")

        def _get_vehicle_for_client(user):
            # zwraca tylko dostępne pojazdy
            print("Zwracam tylko dostępne pojazdy dla klienta")

        def get_vehicle(user):
            if user.role in ("Admin", "Seller"):
                return _get_vehicle_for_admin_seller(user)
            elif user.role == "Client":
                return _get_vehicle_for_client(user)
            else:
                print("Brak dostępu")







def require_roles(*allowed_roles):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user.role not in allowed_roles:
                print(f"Brak dostępu dla roli: {user.role}")
                return None  # lub wyjątek, albo komunikat GUI
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@require_roles("Admin", "Seller")
def edit_vehicle(user, vehicle_id):
    # kod edycji pojazdu
    pass

@require_roles("Client")
def rent_vehicle(user, vehicle_id):
    # kod wypożyczenia
    pass