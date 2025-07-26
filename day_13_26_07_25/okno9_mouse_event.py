import tkinter as tk


def on_click(event):
    print(f"Clicked at x ={event.x}, y={event.y}")


root = tk.Tk()
root.title("Mouse Event Example")
root.geometry("400x300")

frame = tk.Frame(root, bg="lightblue", width=300, height=200)
frame.pack()

# dodanie eventu do kliknięcia lewym kalwiszem myszy
frame.bind("<Button-1>", on_click)

tk.Label(frame, text="Click anywhere in this blue area").pack(pady=50)

root.mainloop()
