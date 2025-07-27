from perplexity import Perplexity


def uruchom_dialog():
    print("💬 Witaj! Możesz zadawać pytania. Wpisz 'exit', aby zakończyć.\n")
    p = Perplexity()

    while True:
        pytanie = input("🧠 Ty: ")
        if pytanie.lower().strip() == "exit":
            print("👋 Do zobaczenia!")
            break

        try:
            odpowiedzi = p.search(pytanie)
            print("\n🤖 Copilot:")
            for i, odp in enumerate(odpowiedzi, 1):
                print(f"{i}. {odp.strip()}\n")
        except Exception as e:
            print(f"⚠️ Wystąpił błąd: {e}")

    p.close()

# Uruchomienie programu
if __name__ == "__main__":
    uruchom_dialog()