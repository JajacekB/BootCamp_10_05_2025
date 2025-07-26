import tkinter as tk

from parso.python.tree import Lambda


def on_text_click(event):
    print("Kliknięto tekst", event.x, event.y)


root = tk.Tk()
c=tk.Canvas(root, width=300, height=200, bg="white")
c.pack()

text_id = c.create_text(
    150,100,
    text="kliknij mnie",
    font=("Helvetica",18),
    fill="darkblue"
)

c.tag_bind(text_id, '<Button>', on_text_click)

c.tag_bind(text_id, "<Enter>", lambda e: c.itemconfig(text_id, fill="red"))
c.tag_bind(text_id, "<Leave>", lambda e: c.itemconfig(text_id, fill="darkblue"))

root.mainloop()