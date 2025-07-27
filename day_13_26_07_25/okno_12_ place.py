import tkinter as tk

root = tk.Tk()
root.title("Place Layout Example")
root.geometry("400x300")

tk.Label(root, text="Absolute Position", bg="Lightblue").place(x=50, y=50)

tk.Button(root, text="Relattve Position").place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()
