import tkinter as tk


root = tk.Tk()
root.title("Pack layout Example")
root.geometry("400x300")

tk.Label(root, text="Top", bg="red").pack(side=tk.TOP, fill=tk.X)
tk.Label(root, text="Bottom", bg="blue", fg="white").pack(side=tk.BOTTOM, fill=tk.X)
tk.Label(root, text="Left", bg="green", fg="white").pack(side=tk.LEFT, fill=tk.Y)
tk.Label(root, text="Right", bg="purple", fg="white").pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(root, text="Center", bg="yellow").pack(expand=True)
# tk.Label(root, text="Center", bg="yellow").pack()


root.mainloop()
