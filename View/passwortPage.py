import tkinter as tk
import os


def lade_passwort():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pfad = os.path.join(base_dir, "..", "passwort.txt")  
        pfad = os.path.abspath(pfad)
        with open(pfad, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("passwort.txt nicht gefunden!")
        return None


class PasswortPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.passwort = lade_passwort()
        self.eingabe = ""
        self.zielseite = None

        self.kreise = []
        self.erzeuge_ui()

    def erzeuge_ui(self):
        # Grid-Layout für das gesamte Frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=0)  # Back Button
        self.rowconfigure(1, weight=0)  # Anzeige Kreise
        self.rowconfigure(2, weight=1)  # Buttons

        # Back Button oben links
        back_button = tk.Button(self, text="← Zurück", font=("Arial", 16, "bold"), bg="#d3d3d3",
                                command=lambda: self.controller.show_page("HomePage"))
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Anzeige Kreise (für Passwortlänge)
        kreise_frame = tk.Frame(self)
        kreise_frame.grid(row=1, column=0, columnspan=3, pady=20)
        for i in range(6):
            lbl = tk.Label(kreise_frame, text="○", font=("Arial", 28), width=2)
            lbl.grid(row=0, column=i, padx=8)
            self.kreise.append(lbl)

        # Button-Frame für Zahlen
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=3)

        # Zahlen-Buttons 1-9 in 3x3 Grid
        btn_font = ("Arial", 24, "bold", )
        btn_width = 8
        btn_height = 4


        for i in range(9):
            btn = tk.Button(self.button_frame, text=str(i + 1), font=btn_font,
                            width=btn_width, height=btn_height, bg="#a0a0a0",
                            command=lambda n=i + 1: self.zahl_gedrueckt(str(n)))
            btn.grid(row=i // 3, column=i % 3, padx=8, pady=8)

        # Button 0 in der Mitte unten
        btn0 = tk.Button(self.button_frame, text="0", font=btn_font,
                         width=btn_width, height=btn_height, bg="#a0a0a0",
                         command=lambda: self.zahl_gedrueckt("0"))
        btn0.grid(row=3, column=1, padx=8, pady=8)

        # Löschen-Button rechts unten
        loeschen_btn = tk.Button(self.button_frame, text="←", font=btn_font,
                                 width=btn_width, height=btn_height, bg="#a0a0a0",
                                 command=self.loeschen)
        loeschen_btn.grid(row=3, column=2, padx=8, pady=8)


    def zahl_gedrueckt(self, zahl):
        if len(self.eingabe) < 6:
            self.eingabe += zahl
            self.kreise[len(self.eingabe) - 1].config(text="●")

        if len(self.eingabe) == 6:
            self.after(300, self.pruefe_passwort)


    def loeschen(self):
        if len(self.eingabe) > 0:
            self.kreise[len(self.eingabe) - 1].config(text="○")
            self.eingabe = self.eingabe[:-1]


    def pruefe_passwort(self):
        if self.eingabe == self.passwort:
            if self.zielseite:
                self.controller.show_page(self.zielseite)
        else:
            print("Falsch!")
            self.shake()
            self.eingabe = ""
            for lbl in self.kreise:
                lbl.config(text="○")


    def set_weiterleitungsziel(self, seite_name):
        self.zielseite = seite_name


    def zuruecksetzen(self):
        self.eingabe = ""
        for lbl in self.kreise:
            lbl.config(text="○")


    def shake(self):
        root = self.winfo_toplevel()
        x = root.winfo_x()
        y = root.winfo_y()

        def move(offsets, i=0):
            if i < len(offsets):
                root.geometry(f"+{x + offsets[i]}+{y}")
                self.after(30, move, offsets, i + 1)
            else:
                root.geometry(f"+{x}+{y}")

        offsets = [-10, 10, -8, 8, -5, 5, -2, 2, 0]
        move(offsets)


