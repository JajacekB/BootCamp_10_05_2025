from datetime import datetime, date


def get_date_from_user(prompt) -> date:
    # f"\nPodaj rzeczywistą datę zwrotu (DD-MM-YYYY) Enter = dziś: "  - przykładowy prompt do użycia
    while True:
        return_date_input_str = input(prompt).strip().lower()

        try:

            if return_date_input_str:
                return_date_input = datetime.strptime(return_date_input_str, "%d-%m-%Y").date()
            else:
                return_date_input = date.today()
            break

        except ValueError:
            print("❌ Niepoprawny format daty.")
            continue
    return return_date_input
