import tkinter as tk
from View.homepage import HomePage
from View.routen import RoutenPage
from View.standort import StandortPage

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
        }
        self.show_page("HomePage")

    

    def show_page(self, page_name):
        for child in self.container.winfo_children():
            child.destroy()

        # Immer neu erstellen
        page_class = self.pages[page_name]
        page = page_class(self.container, self)
        self.active_pages[page_name] = page


        page.grid(row=0, column=0, sticky="nsew")