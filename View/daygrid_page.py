import tkinter as tk
from tkinter import messagebox

class DayGridPage(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Tagesauswahl – Raster")
        self.geometry("600x600")

        self.label = tk.Label(self, text="Tagesauswahl (1–100)", font=("Arial", 14))
        self.label.pack(pady=10)

        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack()

        self.erzeuge_grid()

    def erzeuge_grid(self):
        for zeile in range(10):
            for spalte in range(10):
                tag_nummer = zeile * 10 + spalte + 1
                btn = tk.Button(self.grid_frame, text=str(tag_nummer), width=6, height=3,
                                command=lambda n=tag_nummer: self.tag_geklickt(n))
                btn.grid(row=zeile, column=spalte, padx=2, pady=2)

    def tag_geklickt(self, tag):
        messagebox.showinfo("Tag gewählt", f"Du hast Tag {tag} gewählt!")
