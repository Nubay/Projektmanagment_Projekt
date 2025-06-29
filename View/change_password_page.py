import tkinter as tk
from tkinter import messagebox
from Controller.passwort_controller import speichere_passwort
from View.Components.benachrichtigung import NotificationDialog


class ChangePasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.eingabe = ""

        # Layout-Konfiguration
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=0)  # Back + Titel
        self.rowconfigure(1, weight=0)  # Kreise
        self.rowconfigure(2, weight=1)  # Buttons
        self.rowconfigure(3, weight=0)  # Speichern-Button

        # Zurück-Button oben links
        back_button = tk.Button(
            self, text="← Zurück", font=("Arial", 16, "bold"), bg="#d3d3d3",
            command=lambda: self.controller.show_page("SettingsPage")
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Titel zentriert
        title = tk.Label(self, text="Passwort ändern", font=("Arial", 32, "bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="n", pady=20)

        # Anzeige der eingegebenen Kreise (6 Stellen)
        self.kreise = []
        kreise_frame = tk.Frame(self)
        kreise_frame.grid(row=1, column=0, columnspan=3, pady=20)
        for i in range(6):
            lbl = tk.Label(kreise_frame, text="○", font=("Arial", 28), width=2)
            lbl.grid(row=0, column=i, padx=8)
            self.kreise.append(lbl)

        # Zahlen-Buttons 1-9 in 3x3 Grid
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=3)

        btn_font = ("Arial", 24, "bold")
        btn_width = 8
        btn_height = 4
        btn_bg = "#a0a0a0"

        for i in range(9):
            btn = tk.Button(button_frame, text=str(i + 1), font=btn_font,
                            width=btn_width, height=btn_height, bg=btn_bg,
                            command=lambda n=i + 1: self.zahl_gedrueckt(str(n)))
            btn.grid(row=i // 3, column=i % 3, padx=8, pady=8)

        # Button 0 in der Mitte unten
        btn0 = tk.Button(button_frame, text="0", font=btn_font,
                         width=btn_width, height=btn_height, bg=btn_bg,
                         command=lambda: self.zahl_gedrueckt("0"))
        btn0.grid(row=3, column=1, padx=8, pady=8)

        # Löschen-Button rechts unten
        loeschen_btn = tk.Button(button_frame, text="←", font=btn_font,
                                 width=btn_width, height=btn_height, bg=btn_bg,
                                 command=self.loeschen)
        loeschen_btn.grid(row=3, column=2, padx=8, pady=8)

        # Speichern-Button unten
        speichern_btn = tk.Button(
            self, text="Speichern", command=self.speichern_passwort,
            font=("Arial", 20), width=20, height=2,
            bg="#a0a0a0", activebackground="#808080"
        )
        speichern_btn.grid(row=3, column=0, columnspan=3, pady=20, sticky="n")

    def zahl_gedrueckt(self, zahl):
        if len(self.eingabe) < 6:
            self.eingabe += zahl
            self.kreise[len(self.eingabe) - 1].config(text="●")

    def loeschen(self):
        if len(self.eingabe) > 0:
            self.kreise[len(self.eingabe) - 1].config(text="○")
            self.eingabe = self.eingabe[:-1]

    def speichern_passwort(self):
        if len(self.eingabe) != 6:
            NotificationDialog(self, message="Passwort muss 6 Zeichen lang sein.")
            return
        try:
            speichere_passwort(self.eingabe)
            NotificationDialog(self, message="Passwort erfolgreich gespeichert!")
        except Exception as e:
            NotificationDialog(self, message="Passwort konnte nicht gespeichert werden.")
            print("Fehler beim Speichern:", e)

        self.eingabe = ""
        for lbl in self.kreise:
            lbl.config(text="○")

