import tkinter as tk

root = tk.Tk()
root.title("Label Example")
root.geometry("400x200")

label = tk.Label(root, text="Hello there")

label.pack()

root.mainloop()