import tkinter as tk
from tkinter import messagebox
from View.daygrid_page import DayGridPage
from View.overview_page import OverviewPage
from Controller.passwort_controller import speichere_passwort

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        tk.Button(self, text="Automatikmodus").grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        tk.Button(self, text="Passwort ändern", command=self.open_passwort_fenster).grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        tk.Button(self, text="Tagesauswahl", command=self.open_day_grid).grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tk.Button(self, text="Übersicht anzeigen", command=self.zeige_übersicht).grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    def open_day_grid(self):
        DayGridPage()

    def zeige_übersicht(self):
        fenster = tk.Toplevel(self)
        fenster.title("Übersicht")
        page = OverviewPage(fenster)
        page.pack(expand=True, fill="both")

    def open_passwort_fenster(self):
        fenster = tk.Toplevel(self)
        fenster.title("Passwort ändern")
        fenster.geometry("400x150")

        label = tk.Label(fenster, text="Neues Passwort (min. 6 Zeichen):")
        label.pack(pady=10)

        entry = tk.Entry(fenster, show="*", width=30)
        entry.pack(pady=5)

        def speichern():
            passwort = entry.get()
            if len(passwort) < 6:
                messagebox.showwarning("Fehler", "Das Passwort muss mindestens 6 Zeichen lang sein.")
                return
            speichere_passwort(passwort)
            messagebox.showinfo("Erfolg", "Passwort gespeichert!")
            fenster.destroy()

        speichern_btn = tk.Button(fenster, text="Speichern", command=speichern)
        speichern_btn.pack(pady=10)
