import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import cv2 as cv
from PIL import Image, ImageTk
from datetime import datetime
import requests
import json
import re

from logs import  logging
from api_logic import ApiLogic
from utils import transliterate
from styles import Styles, Themes
from add_form import AddForm


logger = logging.getLogger(__name__)

class App(ApiLogic):
    def __init__(self, window: tk.Tk, camera_source: int = 0):
        super().__init__(camera_source)
        if not self.cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось открыть камеру", parent=window)
        self.show_alert = False
        self.is_running = True
        self.window = window
        self.window.title("Face Recognition Client")
        
        
        self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.styles = Styles(Themes.PASTEL)
        
        self.photo = None
        self.delay = 15

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.frame = ttk.Frame(self.window, padding=10, style="Main.TFrame")
        self.frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height, bg="#F5F5F5", highlightthickness=0)
        self.canvas.pack(fill="both", side="right", expand=True, padx=10, pady=10)

        self.button_frame = ttk.Frame(self.frame, style="Main.TFrame")
        self.button_frame.pack(side="top", fill="y", padx=10, pady=10)
        
        self.btn_snapshot = ttk.Button(self.button_frame, text="Скриншот", command=self.screenshot, width=15)
        self.btn_snapshot.pack(side="top", pady=5)
        self.btn_add = ttk.Button(self.button_frame, text="Добавить\nпользователя", command=self.open_add_window, width=15)
        self.btn_add.pack(side="top", pady=5)

    def update(self):
        if not self.is_running:
            return
        frame = super().update()
        if frame is not None:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        if self.task:
            self.thread_pool.submit(self.show_response)
        self.window.after(self.delay, self.update)


    def show_response(self):
        if self.show_alert:
            return
        self.show_alert = True
        try:
            resp: requests.Response = self.task.result(timeout=3)
            data = resp.json()
            if resp.status_code == 200:
                surname, name = transliterate(data["name"], "en2ru").split("_")
                name = name[0].upper() + name[1:]
                surname = surname[0].upper() + surname[1:]
                messagebox.showinfo("Пользователь найден",
                                    f"Добро пожаловать\n{name} {surname}",
                                    parent=self.window)
            elif resp.status_code == 404:
                messagebox.showwarning("Неизвестный пользователь",
                                        "Отказано в доступе",
                                        parent=self.window)
        except Exception as e:
            logger.error(f"Ошибка обработки ответа: {e}")
            messagebox.showerror("Ошибка",
                                "Не удалось обработать ответ сервера",
                                parent=self.window)
        self.show_alert = False

    def open_add_window(self):
        self.is_running = False
        self.window.withdraw()
        AddForm(self.window, self.styles, self.back_to_root)

    def back_to_root(self):
        self.is_running = True
        self.update()
        self.window.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.title("CamCap")
    # root.geometry("1000x700+250+100")
    root.mainloop()