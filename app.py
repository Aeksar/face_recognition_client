import tkinter as tk
from tkinter import messagebox, filedialog
import cv2 as cv
from PIL import Image, ImageTk
from datetime import datetime
import requests
import json
import re

from logs import  logging
from api_logic import ApiLogic
from utils import transliterate


class App(ApiLogic):
    
    def __init__(self, window: tk.Tk, camera_source: int=0):
        super().__init__(camera_source)   
        if not self.cap.isOpened():
            messagebox.showinfo("Ошибка", "Не удалось открыть камеру")
        self.show_alert = False
        self.is_running = True
        
        self.window = window

        self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        self.frame = tk.Frame(self.window)
        self.frame.pack(side="left", fill="both")
        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height+10)
        self.canvas.pack(fill="both", side="right", expand=True)

        self.btn_snapshot = tk.Button(self.frame, text="Скриншот", height=2, width=12, command=self.screenshot)
        self.btn_snapshot.pack(side="top")
        self.btn_add = tk.Button(self.frame, text="Добавить\nпользователя", command=self.open_add_window, height=3, width=12)
        self.btn_add.pack(side="top")
        self.photo = None
        self.delay = 15
        self.update()

    def update(self):
        if not self.is_running:
            return
        frame = super().update()         
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        if self.task:
            self.thread_pool.submit(self.show_response)
        self.window.after(self.delay, self.update)


    def show_response(self):
        if not self.show_alert:
            self.show_alert = True
            resp: requests.Response = self.task.result(timeout=3)
            data = resp.json()
            if resp.status_code == 200:
                surname, name = transliterate(data["name"], "en2ru").split("_")
                name = name[0].upper() + name[1:]
                surname = surname[0].upper() + surname[1:]
                messagebox.showinfo("Пользователь найден", f"Добро пожаловать\n{name} {surname}")
            elif resp.status_code == 404:
                messagebox.showwarning("Неизвестный пользователь", "Отказано в доступе")
            self.show_alert = False
            
    def open_add_window(self):
        self.is_running = False
        self.window.withdraw()
        self.opened_window = tk.Toplevel(self.window)
        
        self.name_label = tk.Label(self.opened_window, text="Имя:")
        self.name_entry = tk.Entry(self.opened_window)
        self.surname_label = tk.Label(self.opened_window, text="Фамилия:")
        self.surname_entry = tk.Entry(self.opened_window)
        self.image_label = tk.Label(self.opened_window, text="Фото:")
        self.filename = tk.Entry(self.opened_window)
        
        
        self.name_label.grid(column=0, row=0, padx=5, pady=5)
        self.surname_label.grid(column=0, row=1, padx=5, pady=5)
        self.name_entry.grid(column=1, row=0, padx=5, pady=5)
        self.surname_entry.grid(column=1, row=1, padx=5, pady=5)
        self.image_label.grid(column=0, row=2, padx=5, pady=5)
        self.filename.grid(column=1, row=2, padx=5, pady=5)
        
        submit_btn = tk.Button(self.opened_window, text="Создать", command=self.add_user)
        back_btn = tk.Button(self.opened_window, text="Назад", command=lambda: self.back_to_root())
        submit_btn.grid(column=0, row=3, padx=5, pady=5)
        back_btn.grid(column=1, row=3, padx=5, pady=5)
        
        
    def add_user(self):
        filename = self.filename.get()
        name = "_".join([self.name_entry.get(), self.surname_entry.get()])
        if not re.match(r"[А-я]", name):
            name = transliterate(name, "ru2en")
        file = cv.imread(filename)
        file = self.frame2bytes(file)
        resp = self.add_face(name, file)
        self.back_to_root()
        if resp.status_code == 201:
            messagebox.showinfo("Успех", " Пользователь добавлен")
        else:
            messagebox.showwarning("Ошибка", "Пользователь не был добавлен")
    
    def back_to_root(self):
        self.opened_window.destroy() 
        self.is_running = True
        self.update()
        self.window.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.title("CamCap")
    # root.geometry("1000x700+250+100")
    root.mainloop()