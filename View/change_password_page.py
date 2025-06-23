import tkinter as tk
from tkinter import messagebox
from Controller.passwort_controller import speichere_passwort

class ChangePasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Layout-Konfiguration
        self.columnconfigure(0, weight=1)
        for row in range(10):
            self.rowconfigure(row, weight=1)

        # Zurück-Button
        back_button = tk.Button(
            self, text="← Zurück", font=("Arial", 16, "bold"), bg="#d3d3d3",
            command=lambda: self.controller.show_page("SettingsPage")
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Titel
        title = tk.Label(self, text="Passwort ändern", font=("Arial", 32, "bold"))
        title.grid(row=0, column=0, sticky="n", pady=20)

        # Label (weniger Abstand nach unten)
        label = tk.Label(self, text="Neues Passwort (min. 6 Zeichen):", font=("Arial", 24))
        label.grid(row=2, column=0, pady=(3, 0))

        # Eingabefeld (breiter und höher)
        self.entry = tk.Entry(self, show="*", font=("Arial", 20), width=50,
                              bg="white", fg="black",
                              relief="solid", bd=2,
                              )
        self.entry.grid(row=3, column=0, pady=(0, 5), ipady=8)  # Mehr Innenhöhe, weniger Abstand unten

        # Speichern-Button (etwas höher, weniger Abstand oben)
        speichern_btn = tk.Button(
            self, text="Speichern", command=self.speichern_passwort,
            font=("Arial", 20), width=20, height=2,
            bg="#a0a0a0", activebackground="#808080"
        )
        speichern_btn.grid(row=4, column=0, pady=(10, 20))  # Oben 10, unten 20

    def speichern_passwort(self):
        passwort = self.entry.get()
        if len(passwort) < 6:
            messagebox.showwarning("Fehler", "Das Passwort muss mindestens 6 Zeichen lang sein.")
            return
        speichere_passwort(passwort)
        messagebox.showinfo("Erfolg", "Passwort gespeichert!")
        self.entry.delete(0, tk.END)
