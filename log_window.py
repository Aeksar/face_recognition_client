import tkinter as tk
from tkinter import ttk
from typing import Callable
import re

from api_base import ApiHandler
from utils import transliterate


class LogWindow(ApiHandler):
    def __init__(self, root_window: tk.Tk, on_close: Callable[[], None]):
        super().__init__()
        self.root_window = root_window
        self.on_close = on_close
        self.window = None
        self.filename = None
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.root_window)
        self.window.title("Журнал доступа")
        self.window.geometry("600x500")

        frame = ttk.Frame(self.window, padding=20, style="Main.TFrame")
        frame.pack(fill="both", expand=True)

        filter_frame = ttk.Frame(frame, style="Main.TFrame")
        filter_frame.pack(side="top", fill="x", pady=5)

        ttk.Label(filter_frame, text="От:").pack(side="left", padx=5, pady=5)
        self.start_time_entry = ttk.Entry(filter_frame, width=20)
        self.start_time_entry.pack(side="left", padx=5, pady=5)
        ttk.Label(filter_frame, text="До:").pack(side="left", padx=5, pady=5)
        self.end_time_entry = ttk.Entry(filter_frame, width=20)
        self.end_time_entry.pack(side="left", padx=5, pady=5)
        ttk.Label(filter_frame, text="(ГГГГ-ММ-ДД ЧЧ:ММ:СС)").pack(side="left", padx=5, pady=5)
        
        name_frame = ttk.Frame(frame, style="Main.TFrame")
        name_frame.pack(fill="x", pady=5)
        ttk.Label(name_frame, text="Имя:").pack(side="left", padx=5)
        self.name_filter_entry = ttk.Entry(name_frame, width=30)
        self.name_filter_entry.pack(side="left", padx=5)
        
        filter_button_frame = ttk.Frame(frame, style="Main.TFrame")
        filter_button_frame.pack(fill="x", pady=5)
        filter_btn = ttk.Button(filter_button_frame, text="Фильтр", command=self.load_logs)
        filter_btn.pack(side="left", padx=5)
        reset_btn = ttk.Button(filter_button_frame, text="Сброс", command=self.reset_filters)
        reset_btn.pack(side="left", padx=5)

        columns = ("time", "name", "access")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", style="Treeview")
        self.tree.heading("time", text="Время")
        self.tree.heading("name", text="Имя")
        self.tree.heading("access", text="Доступ")
        self.tree.column("time", width=150, anchor="center")
        self.tree.column("name", width=200, anchor="center")
        self.tree.column("access", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)

        button_frame = ttk.Frame(frame, style="Main.TFrame")
        button_frame.pack(fill="x", pady=10)
        close_btn = ttk.Button(button_frame, text="Назад", command=self.back_to_root)
        close_btn.pack(side="right")

        self.load_logs()

    def reset_filters(self):
        self.name_filter_entry.delete(0, tk.END)
        self.start_time_entry.delete(0, tk.END)
        self.end_time_entry.delete(0, tk.END)
        self.load_logs()
    
    def load_logs(self):
        start = self.start_time_entry.get()
        end = self.end_time_entry.get()
        name = self.name_filter_entry.get()
        
        if re.match(r"[А-Яа-я]+", name):
            name = transliterate(name, "ru2en")
            name = name.title()    
         
        logs = self.get_log(start, end, name)
        
        for item in self.tree.get_children():
            self.tree.delete(item) 
            
        for log in logs:
            time = log["time"]
            name = log["name"]
            success = log["success"]
            status = "Разрешён" if success else "Запрещён"
            if re.match(r"^[A-Za-z]+_[A-Za-z]+$", name):
                surname, name = transliterate(name, "en2ru").split("_")
                name = f"{surname.capitalize()} {name.capitalize()}"
            self.tree.insert("", "end", values=(time, name, status))
    
    def back_to_root(self):
        self.window.destroy()
        self.on_close()