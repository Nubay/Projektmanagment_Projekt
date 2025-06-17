import tkinter as tk
from tkinter import messagebox
from Controller.passwort_controller import speichere_passwort

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # Automatikmodus & Passwort ändern mit größerer Schrift
        tk.Button(self, text="Automatikmodus", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        tk.Button(self, text="Passwort ändern", command=self.open_passwort_fenster, font=("Arial", 20)).grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def open_passwort_fenster(self):
        fenster = tk.Toplevel(self)
        fenster.title("Passwort ändern")
        fenster.state("zoomed") 
        fenster.resizable(False, False)

        label = tk.Label(fenster, text="Neues Passwort (min. 6 Zeichen):", font=("Arial", 20))
        label.pack(pady=30)

        entry = tk.Entry(fenster, show="*", font=("Arial", 20), width=30)
        entry.pack(pady=10)

        def speichern():
            passwort = entry.get()
            if len(passwort) < 6:
                messagebox.showwarning("Fehler", "Das Passwort muss mindestens 6 Zeichen lang sein.")
                return
            speichere_passwort(passwort)
            messagebox.showinfo("Erfolg", "Passwort gespeichert!")
            fenster.destroy()

        speichern_btn = tk.Button(fenster, text="Speichern", command=speichern, font=("Arial", 18), width=20, height=2)
        speichern_btn.pack(pady=30)








