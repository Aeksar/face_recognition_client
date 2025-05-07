import tkinter as tk
from tkinter import messagebox
import cv2 as cv
from PIL import Image, ImageTk
from datetime import datetime
from api_logic import ApiLogic
import requests
from logs import  logging


class App(ApiLogic):
    def __init__(self, window: tk.Tk, camera_source: int=0):
        super().__init__(camera_source)   
        if not self.cap.isOpened():
            messagebox.showinfo("Ошибка", "Не удалось открыть камеру")
    
        self.window = window

        self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        self.frame = tk.Frame(self.window)
        self.frame.pack(side="left", fill="both")
        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height+10)
        self.canvas.pack(fill="both", side="right", expand=True)

        self.btn_snapshot = tk.Button(self.frame, text="Снимок", height=2, width=10, command=self.screenshot)
        self.btn_snapshot.pack(side="right")

        self.photo = None
        self.delay = 30
        self.update()

    def update(self):
        frame = super().update()         
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)  
        self.window.after(self.delay, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.title("CamCap")
    root.geometry("1000x700+250+100")
    root.mainloop()