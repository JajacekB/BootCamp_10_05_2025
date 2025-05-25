import shutil
from pathlib import Path

base_path = Path('../ops_example')
base_path2 = Path('ops_example/D')

if base_path.exists() and base_path.is_dir():
    shutil.rmtree(base_path)

base_path.mkdir()

path_b = base_path / 'A' / 'B'
path_c = base_path / 'A' / 'C'
path_d = base_path / 'A' / 'D'

# path_b.mkdir()

path_b.mkdir(parents=True)
path_c.mkdir()

for filename in ('ex1.txt', 'ex2.txt', 'ex3.txt'):
    with open(path_b / filename, "w", encoding='utf-8') as stream:
        stream.write(f"Jakaś treść w pliku {filename}")

shutil.move(path_b, path_d)
shutil.copy(path_d / 'ex1.txt', path_c / 'ex1.txt')

ex1 = path_d / "ex1.txt"
ex1.rename(ex1.parent / 'ex1rename.log')


print(base_path.absolute())
print(base_path.name)
print((base_path.parent.absolute()))

print("-----")
print(base_path.suffix)
print(ex1.suffix)
print(base_path.parts)
print(base_path2.parts)

path_abs = r"C:\Users\Jacek\PycharmProjects\BootCamp_10_05_2025\ops_example\A\D\ex1rename.log"
with open(path_abs, "r") as f:
    lines = f.read()

print(lines)
# "C:\\Users\\Jacek\\PycharmProjects\\BootCamp_10_05_2025\\ops_example\\A\\D\\ex1rename.log"  - ścieżka windows
# r"C:\Users\Jacek\PycharmProjects\BootCamp_10_05_2025\ops_example\A\D\ex1rename.log"  - "r" przed ścieżką windows raw string


