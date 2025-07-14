from prace_domowe.fleet_manager_v2_1.fleet_database import engine
from fleet_models_db import *

# Tworzenie tabel w bazie danych
Base.metadata.create_all(engine)
print("Baza danych i tabele zostały utworzone.")