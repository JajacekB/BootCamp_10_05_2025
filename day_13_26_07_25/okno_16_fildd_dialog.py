import os.path
import tkinter as tk
from tkinter import filedialog

# WYŁĄCZ natywny macOS dialog
os.environ['TK_SILENCE_DEPRECATION'] = '1'
os.environ['TK_USE_NATIVE_DIALOG'] = '0'


def wybierz_plik():
    # start_dir = os.path.expanduser("~/Documents")
    start_dir = os.getcwd()  # otwiera filedialog w miejscu uruchomienia skryptu
    plik = filedialog.askopenfilename(
        title="Wybierz plik",
        initialdir=start_dir,
        # filetypes=[("Wszystkie pliki", "*.*")])
        filetypes=[
            ("Pliki tekstowe", "*.txt"),
            ("Wszystkie pliki", "*")
        ]
    )
    root.deiconify()  # powrót naszego okienka
    if plik:
        print(f"Wybrano plik: {plik}")
        label_path.config(text=f"Wybrano: {plik}")
    else:
        label_path.config(text="Nie wybrano pliku")


root = tk.Tk()
root.title("Demo wyboru pliku")

label_path = tk.Label(root, text="Brak pliku", wraplength=400)
label_path.pack(padx=20, pady=(20, 10))

btn_again = tk.Button(root, text="Wybierz plik ponownie",
                      command=lambda: [root.withdraw(), wybierz_plik()])
btn_again.pack(pady=(0, 20))

root.withdraw()  # ukrycie głownego okienka
wybierz_plik()
# Wybrano plik: /Users/radoslawjaniak/Documents/1.png

root.mainloop()
