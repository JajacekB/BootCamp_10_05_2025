import tkinter as tk

def show_text():
    text = entry.get()
    print(f"Wprowadzamy tekst: {text}")

app = tk.Tk()
app.title("Pokaż co potrafisz")

entry = tk.Entry(app)
entry.pack()

button = tk.Button(app, text="Pokaż tekst", command=show_text)
button.pack()

app.mainloop()