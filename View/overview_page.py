import tkinter as tk
import os
import glob

class OverviewPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = tk.Label(self, text="Gespeicherte Routen", font=("Arial", 14))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self, font=("Arial", 12), width=40, height=20)
        self.listbox.pack(pady=10)

        self.lade_routen()

    def lade_routen(self):
        folder = "Model/JsonDateinTage"
        json_files = sorted(glob.glob(os.path.join(folder, "*.json")))
        for file in json_files:
            dateiname = os.path.basename(file)
            self.listbox.insert(tk.END, dateiname)


