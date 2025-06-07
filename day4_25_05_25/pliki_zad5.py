from pathlib import Path

folder_path = Path("katalog")

txt_files = list(folder_path.glob("*.txt"))
print(f" Pliki txt {[f.name for f in txt_files]}")
# Pliki .txt: ['file_1.txt', 'nowy.txt', 'results.txt']

for file_path in txt_files:
    content = file_path.read_text(encoding='utf-8')
    print(f"Pliki {file_path.name}, rozmiar: {len(content)} znaków.")
# Plik: file_1.txt, rozmiar: 0 znaków.
# Plik: nowy.txt, rozmiar: 9 znaków.
# Plik: results.txt, rozmiar: 6 znaków.
# Przerwa 5 minut 15:05

