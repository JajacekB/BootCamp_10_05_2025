from fleet_database import engine, Base
from fleet_models import *

# Tworzenie tabel w bazie danych
Base.metadata.create_all(engine)
print("Baza danych i tabele zostały utworzone.")