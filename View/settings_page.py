import tkinter as tk
from tkinter import messagebox

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Grid-Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # Zurück-Button oben links
        back_button = tk.Button(self, text="← Zurück", font=("Arial", 14, "bold"), bg="#d3d3d3",
                                command=lambda: self.controller.show_page("HomePage"))
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Titel zentriert
        title_label = tk.Label(self, text="Einstellungen", font=("Arial", 32, "bold"))
        title_label.grid(row=0, column=0, sticky="n", pady=20)


        # Automatikmodus-Button
        automatik_button = tk.Button(
            self, text="Automatikmodus", font=("Arial", 24, "bold"),
            bg="#a0a0a0", activebackground="#808080", height=3
        )
        automatik_button.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)

        # Passwort ändern-Button
        passwort_button = tk.Button(
            self, text="Passwort ändern", font=("Arial", 24, "bold"),
            command=lambda: self.controller.show_page("ChangePasswordPage"), bg="#a0a0a0", activebackground="#808080", height=3
        )
        passwort_button.grid(row=2, column=0, sticky="nsew", padx=40, pady=20)









