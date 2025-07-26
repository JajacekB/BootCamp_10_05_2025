import tkinter as tk

def on_value_change(value):
    print(f"Zmienna wartość suwak {value}")

app = tk.Tk()
app.title("przykład suwaka")

slider = tk.Scale(app, from_=0, to=100, orient=tk.HORIZONTAL, command=on_value_change)
slider.pack(side=tk.BOTTOM)

app.mainloop()