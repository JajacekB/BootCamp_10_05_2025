import tkinter as tk
from tkinter import filedialog
import os.path

from docutils.nodes import title


def wybierz_plik():
    start_dir = os.path.expanduser("~/Documents")
    plik = filedialog.askopenfilename(
        title="Wybierz plik",
        initialdir=start_dir,
        filetypes=[("Wszystkie pliki", "*.*""")])
    root.deiconify()
    if plik:
        print(f"Wybrano pli: {plik}")
        label_path.config(text=f"Wybrano: {plik}")
    else:
        label_path.config(text="Nie wybrano pliku")


root = tk.Tk()
root.title("Demo wyboru pliku")

label_path = tk.Label(root, text="Brak plików", wraplength=400)
label_path.pack(padx=20, pady=(20, 10))

btn_again = tk.Button(root, text="Wybierz plik ponownie",
                    command=lambda: [root.withdraw(), wybierz_plik()])
btn_again.pack(padx=20, pady=(20, 10))



root.withdraw()

wybierz_plik()

root.mainloop()