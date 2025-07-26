import tkinter as tk

root = tk.Tk()
root.title("grid Layout Example")
root.geometry("500x200")

tk.Label(root, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root).grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

tk.Button(root, text="Submit").grid(row=2, column=0, columnspan=2, pady=5)

root.grid_columnconfigure(1, weight=1)

root.mainloop()
