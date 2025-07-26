import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime


class CustomEntry(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        style = ttk.Style()
        style.configure("Custom.TEntry", fieldbackground='#ffffff', foreground='#333333')
        style.configure("Custom.TButton", fieldbackground='#dddddd', foreground='#333333')

        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var,
                    style='Custom.TEntry', width=16)
        self.entry.pack(side="left", fill='x', expand=True)

        self.btn = ttk.Button(self, text="▼", command=self.show_calendar,
                    style="Custom.TButton", width=2)
        self.btn.pack(side="left")

        self.entry.bind('<Button-1>', lambda e: self.show_calendar())
        self.calendar_win = None

    def show_calendar(self):
        if self.calendar_win:
            return

        self.calendar_win = tk.Toplevel(self)
        self.calendar_win.transient(self)
        self.calendar_win.grab_set()

        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        self.calendar_win.geometry(f'+{x}+{y}')

        cal = Calendar(self.calendar_win,
                    date_pattern='yyyy-mm-dd',
                    background='#f8f8f8',
                    foreground='#333333',
                    selectbackground='#1976d2',
                    selectforeground='#ffffff')

        cal.pack()

        def select_date():
            selected = cal.get_date()
            self.var.set(selected)
            self.calendar_win.destroy()
            self.calendar_win = None

        cal.bind("<<CalendarSelected>>", lambda e: select_date())

        self.calendar_win.protocol("WM_DELETE_WINDOW",
                                   lambda: self.calendar_win.destroy())
        self.calendar_win.focus_force()

    def get_date(self):
        return self.var.get()


root = tk.Tk()
root.title("Wybór daty")

date_entry = CustomEntry(root)
date_entry.pack(padx=10, pady=10)

result_label = ttk.Label(root, text="Wybrana data: brak")
result_label.pack(pady=5)

def show_result():
    date_str = date_entry.get_date()
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        weekend = dt.strftime("%A")
        formatted = f"Wybrana data: {date_str} - {weekend}"
    except ValueError:
        formatted = "Niepoprawna data"
    result_label.config(text=formatted)

action_btn = ttk.Button(root, text="Pokażw Labelce", command=show_result)
action_btn.pack(pady=5)

root.mainloop()
