import tkinter as tk
from View.homepage import HomePage

class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Navigationssystem")
        self.attributes("-fullscreen", True)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)


        self.pages = {}
        self.show_page(HomePage)

    def show_page(self, PageClass):
        for child in self.container.winfo_children():
            child.destroy()

        page = PageClass(self.container, self)
        page.grid(row=0, column=0, sticky="nsew")
