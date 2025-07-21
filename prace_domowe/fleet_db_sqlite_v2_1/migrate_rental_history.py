import sqlite3
from datetime import date

DB_PATH = "fleet.db"  # ścieżka do twojej bazy SQLite

def migrate_rental_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Dodaj kolumny, jeśli ich nie ma (próbujemy bezpiecznie)
    try:
        cursor.execute("ALTER TABLE rental_history ADD COLUMN actual_return_date DATE")
    except sqlite3.OperationalError:
        pass  # kolumna istnieje

    try:
        cursor.execute("ALTER TABLE rental_history ADD COLUMN base_cost FLOAT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE rental_history ADD COLUMN late_fee FLOAT")
    except sqlite3.OperationalError:
        pass

    conn.commit()

    # 2. Pobierz wszystkie rekordy do migracji
    cursor.execute("""
        SELECT id, planned_return_date, total_cost
        FROM rental_history
    """)
    rows = cursor.fetchall()

    for row in rows:
        rec_id, planned_return_date, total_cost = row

        # Załóżmy:
        # actual_return_date = planned_return_date (brak opóźnienia)
        # base_cost = total_cost (dotychczasowy koszt)
        # late_fee = 0 (na start)
        actual_return_date = planned_return_date
        base_cost = total_cost
        late_fee = 0.0

        # Aktualizuj rekord z nowymi kolumnami
        cursor.execute("""
            UPDATE rental_history SET
                actual_return_date = ?,
                base_cost = ?,
                late_fee = ?,
                total_cost = ?
            WHERE id = ?
        """, (actual_return_date, base_cost, late_fee, total_cost, rec_id))

    conn.commit()
    conn.close()
    print("Migracja rental_history zakończona.")

if __name__ == "__main__":
    migrate_rental_history()