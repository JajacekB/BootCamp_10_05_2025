import tkinter as tk

# mvc - ważne!!!

# okno
root =tk.Tk()

# Header
root.title("Moje okienko")

root.update_idletasks()

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
ww = root.winfo_width()
wh = root.winfo_height()

# Obliczamy pozycję startową
x = (sw - ww) // 2
y = (sh - wh) // 2

root.geometry(f"{ww}x{wh}+{x}+{y}")


# uruchomienie okna
root.mainloop()





