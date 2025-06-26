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
    with open(FILENAME, "w", newline='', encoding="utf-8") as file:
        fieldnames = ["title", "content"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

# Definiowanie funkcji

# Wczytywanie pliku notes.csv
def load_notes():
    with open(FILENAME, "r", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            notes.append(row)

# Zapisywanie pliku notes.csv
def save_notes():
    with open(FILENAME, "w", newline='', encoding="utf-8") as file:
        fieldnames = ["title", "content"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(notes)

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
    print("\nUdało się Cudownie, Wspaniele i Majestatycznie")

# Usuwanie notatek
def remove_note():

    del_number = int(input("\nPodaj numer notatki do usunięcia: ").strip())
    for note in notes:
    if notes[id(note)] == del_number:
        notes.remove(note)
        save_notes()
        print("\nUdało się Cudownie, Wspaniele i Majestatycznie")
        return

# Edycji notatki
def edit_note():

    number_note = int(input("\nPodaj numer notatki do poprawy ").strip())

    note = notes[number_note]
    print(f"F\nEdytujesz; Nazwa: {note['title']} Treść: {note['content']}")
    edit_title = input("\nNowa nazwa? ").strip().capitalize()
    edit_content = input("\nNowa notatka? ").strip()

    if edit_title:
        note["title"] = edit_title
    if edit_content:
        note["content"] = edit_content

    save_notes()
    print("\nUdało się Cudownie, Wspaniele i Majestatycznie")




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