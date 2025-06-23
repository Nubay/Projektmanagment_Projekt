import tkinter as tk
from View.homepage import HomePage
from View.routen import RoutenPage
from View.standort import StandortPage
from View.routen_anzeigen_page import Routen_Anzeigen_Page
from View.settings_page import SettingsPage
from View.change_password_page import ChangePasswordPage


class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.active_pages = {}
        self.title("Navigationssystem")
        self.overrideredirect(True)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)


        self.pages = {
            "HomePage": HomePage,
            "RoutenPage": RoutenPage,
            "StandortPage": StandortPage,
            "Routen_Anzeigen_Page": Routen_Anzeigen_Page,
            "SettingsPage": SettingsPage,
            "ChangePasswordPage": ChangePasswordPage 
        }
        self.show_page("HomePage")

    

    def show_page(self, page_name):
        # Verstecke alle Seiten
        for page in self.active_pages.values():
            page.grid_remove()

        # Seite erstellen, falls noch nicht vorhanden
        if page_name not in self.active_pages:
            page_class = self.pages[page_name]
            page = page_class(self.container, self)
            self.active_pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")
        else:
            self.active_pages[page_name].grid()  # page wieder anzeigen