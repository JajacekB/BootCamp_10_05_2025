from pathlib import Path

folder_path = Path("katalog")

txt_files = list(folder_path.glob("*.txt"))
print(f" Pliki txt {[f.name for f in txt_files]}")

for file_path in txt_files:
    content = file_path.read_text(encoding='utf-8')
    print(f"Pliki {file_path.name}, rozmiar: {len(content)} znaków.")


