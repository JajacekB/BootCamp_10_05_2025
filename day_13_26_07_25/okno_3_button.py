import tkinter as tk


def on_click():
    print("Mój przycisk")

app = tk.Tk()
app.title("Moje okienko")
app.geometry("400x300+100+100")

button = tk.Button(app, text="Kliknij mnie", command=on_click)

button.pack()

app.mainloop()