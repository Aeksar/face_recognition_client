from tkinter import ttk
from enum import Enum

from logs import logging


logger = logging.getLogger(__name__)

class Themes:
    LIGHT = "light"
    DARK = "dark"
    PASTEL = "pastel"


class Styles:
    def __init__(self, theme_name: str = "light"):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.themes = {
            "light": {
                "Main.TFrame": {"background": "#F5F5F5"},
                "TButton": {
                    "background": "#34495E",
                    "foreground": "#FFFFFF",
                    "font": ("Helvetica", 10, "bold"),
                    "padding": 10,
                    "borderwidth": 0
                },
                "TButton.map": {"background": [("active", "#3F6D9E")]},
                "TLabel": {
                    "background": "#F5F5F5",
                    "foreground": "#333333",
                    "font": ("Helvetica", 10)
                },
                "TEntry": {
                    "fieldbackground": "#FFFFFF",
                    "foreground": "#333333",
                    "font": ("Helvetica", 10),
                    "borderwidth": 1,
                    "relief": "solid"
                },
                "window_bg": "#F5F5F5"
            },
            "dark": {
                "Main.TFrame": {"background": "#2C2F33"},
                "TButton": {
                    "background": "#7289DA",
                    "foreground": "#DCDDDE",
                    "font": ("Helvetica", 10, "bold"),
                    "padding": 10,
                    "borderwidth": 0
                },
                "TButton.map": {"background": [("active", "#99AAB5")]},
                "TLabel": {
                    "background": "#2C2F33",
                    "foreground": "#DCDDDE",
                    "font": ("Helvetica", 10)
                },
                "TEntry": {
                    "fieldbackground": "#40444B",
                    "foreground": "#DCDDDE",
                    "font": ("Helvetica", 10),
                    "borderwidth": 1,
                    "relief": "solid"
                },
                "window_bg": "#2C2F33"
            },
            "pastel": {
                "Main.TFrame": {"background": "#FAF3F3"},
                "TButton": {
                    "background": "#A8E6CF",
                    "foreground": "#264653",
                    "font": ("Helvetica", 10, "bold"),
                    "padding": 10,
                    "borderwidth": 0
                },
                "TButton.map": {"background": [("active", "#CFFFD6")]},
                "TLabel": {
                    "background": "#FAF3F3",
                    "foreground": "#264653",
                    "font": ("Helvetica", 10)
                },
                "TEntry": {
                    "fieldbackground": "#FFE6E6",
                    "foreground": "#264653",
                    "font": ("Helvetica", 10),
                    "borderwidth": 1,
                    "relief": "solid"
                },
                "window_bg": "#FAF3F3"
            }
        }
        self.apply_theme(theme_name)

    def apply_theme(self, theme_name: str):
        if theme_name not in self.themes:
            logger.warning(f"Тема {theme_name} не найдена")
            theme_name = "light"
        
        theme = self.themes[theme_name]
        for widget, config in theme.items():
            if widget == "window_bg":
                continue
            if widget.endswith(".map"):
                widget_name = widget.replace(".map", "")
                self.style.map(widget_name, **config)
            else:
                self.style.configure(widget, **config)

    def get_window_bg(self, theme_name: str) -> str:
        return self.themes.get(theme_name, self.themes["light"])["window_bg"]