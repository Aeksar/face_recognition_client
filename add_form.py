import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from logs import logging
import cv2 as cv
import re
from typing import Callable, TYPE_CHECKING

from utils import transliterate 
from api_logic import ApiLogic
from styles import Styles

logger = logging.getLogger(__name__)

class AddForm(ApiLogic):
    def __init__(self, root_window: tk.Tk, styles: Styles, on_close: Callable[[None], None]):
        self.root_window = root_window
        self.styles = styles
        self.on_close = on_close
        self.window = None
        self.filename = None
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.root_window)
        self.window.title("Добавить пользователя")
        self.window.configure(bg="#F5F5F5")
        self.window.geometry("400x250")
        self.window.resizable(False, False)

        form_frame = ttk.Frame(self.window, padding=20, style="Main.TFrame")
        form_frame.pack(fill="both", expand=True)

        self.name_label = ttk.Label(form_frame, text="Имя:")
        self.name_entry = ttk.Entry(form_frame, width=25)
        self.surname_label = ttk.Label(form_frame, text="Фамилия:")
        self.surname_entry = ttk.Entry(form_frame, width=25)
        self.image_label = ttk.Label(form_frame, text="Фото:")
        self.filename_text = ttk.Entry(form_frame, width=25)
        self.filename_btn = ttk.Button(form_frame, text="Выбрать", command=self.get_filename)

        self.name_label.grid(column=0, row=0, padx=5, pady=5, sticky="e")
        self.name_entry.grid(column=1, row=0, padx=5, pady=5)
        self.surname_label.grid(column=0, row=1, padx=5, pady=5, sticky="e")
        self.surname_entry.grid(column=1, row=1, padx=5, pady=5)
        self.image_label.grid(column=0, row=2, padx=5, pady=5, sticky="e")
        self.filename_text.grid(column=1, row=2, padx=5, pady=5)
        self.filename_btn.grid(column=2, row=2, padx=5, pady=5)

        button_frame = ttk.Frame(form_frame, style="Main.TFrame")
        button_frame.grid(column=0, row=3, columnspan=3, pady=10)
        submit_btn = ttk.Button(button_frame, text="Создать", command=self.add_user)
        back_btn = ttk.Button(button_frame, text="Назад", command=self.back_to_root)
        back_btn.pack(side="left", padx=5)
        submit_btn.pack(side="left", padx=5)

    def get_filename(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if self.filename:
            self.filename_text.delete(0, tk.END)
            self.filename_text.insert(0, self.filename)

    def add_user(self):
        filename = self.filename_text.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        if not (surname and name and filename):
            messagebox.showwarning("Ошибка", "Заполните все поля", parent=self.window)
            return
        name = "_".join([name, surname])
        if re.match(r"^[А-Яа-я]+_[А-Яа-я]+$", name):
            name = transliterate(name, "ru2en")
        logger.debug(f"Send request to add user, name: {name}")
        file = cv.imread(filename)
        if file is None:
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение", parent=self.window)
            return
        file = self.frame2bytes(file)
        try:
            resp = self.add_face(name, file)
            self.back_to_root()
            if resp.status_code == 201:
                messagebox.showinfo("Успех", "Пользователь добавлен", parent=self.root_window)
            else:
                messagebox.showwarning("Ошибка", "Пользователь не был добавлен", parent=self.root_window)
        except Exception as e:
            logger.error(f"Ошибка добавления пользователя: {e}")
            messagebox.showerror("Ошибка", "Не удалось связаться с сервером", parent=self.root_window)

    def back_to_root(self):
        self.window.destroy()
        self.on_close()