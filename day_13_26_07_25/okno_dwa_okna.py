import tkinter as tk

root = tk.Tk()
root.title("Głowne okno")

label1 =tk.Label(root, text="to jest głowne okno")
label1.pack(padx=10, pady=10)


second_window = tk.Toplevel(root)
second_window.title("Drugie okienko ")

lebel2 = tk.Label(second_window, text="to jest drugie")
lebel2.pack(padx=10, pady=10)

root.mainloop()