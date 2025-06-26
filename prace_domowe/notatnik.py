# Prosty notatnik z menu
#
# Stwórz aplikację konsolową, która umożliwia:
# 	•	dodawanie notatek (krótki tekst),
# 	•	usuwanie notatek (po numerze/id),
# 	•	edycję notatki,
# 	•	przeglądanie wszystkich notatek.
#
# Użyj pętli while True, prostej listy (lub słownika) oraz funkcji.

import os
import csv

# Deklaracja zmiennych: notatki lista
notes = []

# Deklaracja STAŁYCH: plik csv
FILENAME = "notes.csv"

# Tworzenie pliku jesli nie istnieje
if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline='', encoding="utf-0") as file:
        fieldnames = ["title", "content"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

# Definiowanie funkcji

# Dodawanie notatek
def add_note():
    title = input("\nTytuł notatki ").strip().capitalize()
    content = input("\nTreść notatki ").strip()
    note = {
        "title": title,
        "content": content
    }

    notes.append(note)
    save_notes()
    print("\nUdało się Wspaniele, Cudownie i Majestatycznie")

# Usuwanie notatek
def remove_note():
    while True:
        print("""Jak chcesz usunąć notatkę
        1. Po numerze
        2. Po nazwie
        3. Rezygnuję
        """)

        del_activity = input("\nWybierz ocje (1-3) ").strip()

        match del_activity:
            case 1:
                del_number = input("\nPodaj numer notatki do usunięcia:")
                for note in notes:
                    if notes[id(note)] == del_number:
                        notes.remove(note)
                        save_notes()
                        print("\nUdało się Wspaniele, Cudownie i Majestatycznie")
                        return

            case 2:
                del_title = input("\nPodaj nazwę notatki do usunięcia: ").strip().capitalize()
                for note in notes:
                    if notes["title"] == del_title:
                        notes.remove(note)
                        save_notes()
                        print("\nUdało się Wspaniele, Cudownie i Majestatycznie")
                        return
            case 3:
                return

            case _:
                print("\nZły wybór!!! Zastanów się lepiej.")

# Definowanie funkcji edycji notatki
def edit_note():



# Menu wyboru i głowny program
while True:
    print("""\nCo chcesz zrobić:
    1. Dodaj notatkę
    2. Usuń notatkę
    3. Edytuj notatkę
    4. Wyświetl wszystkie notatki""")

    activiti = input("\nWybierz opcję (1-4): ")

    match activiti:
        case "1":
            add_note()

        case "2":
            remove_note()

        case "3":
            edit_note()

        case "4":
            show_note()

        case _:
            print("\nZły wybór!!! Zastanów się lepiej.")