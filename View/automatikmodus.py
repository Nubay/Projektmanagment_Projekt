import tkinter as tk
from tkinter import ttk
from datetime import datetime
from Model.evaluation import Automatikmodus 
import os
import json


class AutomatikmodusPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.gui_controller = controller

        # Layout-Gewichtung
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)  # Spacer oben (leer, wächst)
        self.rowconfigure(1, weight=0)  # Überschrift + Back-Button (kompakt)
        self.rowconfigure(2, weight=4)  # Eingabe Frame wächst stark
        self.rowconfigure(3, weight=1)  # Status Label (wächst moderat)


        # Überschrift
        title = tk.Label(self, text="Automatikmodus Steuerung", font=("Arial", 32, "bold"))
        title.grid(row=0, column=0, sticky="n", pady=(20, 10))


        # Back Button oben links
        back_button = tk.Button(self, text="← Zurück", font=("Arial", 16, "bold"), bg="#d3d3d3",
                                command=lambda: self.gui_controller.show_page("SettingsPage"))
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)


         # Frame für Eingaben & Button
        input_frame = tk.Frame(self)
        input_frame.grid(row=2, column=0, pady=8, padx=20, sticky="nsew")
        input_frame.columnconfigure(0, weight=1)


        # Innerhalb input_frame die Zeilen so konfigurieren,
        # dass Comboboxen, Button und ggf Spacer gut verteilt sind
        for i in range(5):
            input_frame.rowconfigure(i, weight=0)

        spacer_input = tk.Frame(input_frame)
        spacer_input.grid(row=5, column=0, sticky="nsew")
        input_frame.rowconfigure(5, weight=1)

        # Zeiten mit 15-Minuten-Intervallen erzeugen
        self.zeit_optionen = self.erzeuge_15_minuten_zeiten()

        # Startzeit Label + Combobox
        tk.Label(input_frame, text="Startzeit:", font=("Arial", 24)).grid(row=0, column=0, sticky="w", pady=4)
        self.start_zeit_cb = ttk.Combobox(input_frame, values=self.zeit_optionen, font=("Arial", 40), state="readonly", width=10)
        self.start_zeit_cb.grid(row=1, column=0, sticky="ew", pady=4)
        self.start_zeit_cb.current(0)
        self.start_zeit_cb.option_add("*TCombobox*Listbox*Font", "Arial 40")

        # Endzeit Label + Combobox
        tk.Label(input_frame, text="Endzeit:", font=("Arial", 24)).grid(row=2, column=0, sticky="w", pady=4)
        self.end_zeit_cb = ttk.Combobox(input_frame, values=self.zeit_optionen, font=("Arial", 40), state="readonly", width=10)
        self.end_zeit_cb.grid(row=3, column=0, sticky="ew", pady=4)
        self.end_zeit_cb.current(1)
        self.end_zeit_cb.option_add("*TCombobox*Listbox*Font", "Arial 40")


        # Start/Stopp Button (Toggle)
        self.running = False
        self.toggle_btn = tk.Button(input_frame, text="Start", font=("Arial", 38, "bold"),
                                    bg="#4CAF50", fg="white", width=14,
                                    command=self.toggle_automatikmodus)
        self.toggle_btn.grid(row=4, column=0, pady=(12, 5))

        # Status Label (mehr Platz unten)
        self.status_label = tk.Label(self, text="Status: Nicht gestartet", font=("Arial", 24), fg="blue")
        self.status_label.grid(row=3, column=0, pady=10, sticky="n")

        self.lade_status_und_update_gui()


    def lade_status_und_update_gui(self):
        status_pfad = "Model/JSONAutomatikmodus/status.json"
        default_start = "07:00:00"
        default_end = "16:00:00"

        if os.path.exists(status_pfad):
            with open(status_pfad, "r", encoding="utf-8") as f:
                status = json.load(f)

            running = status.get("running", False)
            start = status.get("start_time", default_start)
            end = status.get("end_time", default_end)

        else:
            running = False
            start = default_start
            end = default_end

        # Setze Comboboxen auf die geladenen Zeiten
        if start in self.zeit_optionen:
            self.start_zeit_cb.current(self.zeit_optionen.index(start))
        else:
            self.start_zeit_cb.set(start)  # Falls Zeit nicht in Liste, einfach anzeigen

        if end in self.zeit_optionen:
            self.end_zeit_cb.current(self.zeit_optionen.index(end))
        else:
            self.end_zeit_cb.set(end)

        # Button und Statuslabel anpassen
        if running:
            self.running = True
            self.toggle_btn.config(text="Stoppen", bg="#f44336")
            self.status_label.config(text=f"Automatikmodus läuft von {start} bis {end}", fg="green")
            # Automatikmodus-Instanz initialisieren mit geladenen Zeiten
            self.auto_instanz = Automatikmodus(start, end, self.gui_controller.home_page, self)
            self.after(500, self.auto_instanz.starten)
            self.auto_instanz.running = True
            self.auto_instanz.started = True  # Falls schon gestartet (optional)
        else:
            self.running = False
            self.toggle_btn.config(text="Start", bg="#4CAF50")
            self.status_label.config(text="Status: Nicht gestartet", fg="blue")
            self.auto_instanz = None



    def erzeuge_15_minuten_zeiten(self):
        zeiten = []
        for stunde in range(24):
            for minute in range(0, 60, 5):
                zeiten.append(f"{stunde:02d}:{minute:02d}:00")
        return zeiten



    def toggle_automatikmodus(self):
        start = self.start_zeit_cb.get()
        ende = self.end_zeit_cb.get()

        if not self.running:
            if start == ende or start > ende:
                self.status_label.config(text="Fehler: Startzeit muss vor Endzeit liegen!", fg="red")
                return

            self.auto_instanz = Automatikmodus(start, ende, self.gui_controller.active_pages["HomePage"], self)
            self.auto_instanz.starten()
            self.running = True
            self.toggle_btn.config(text="Stoppen", bg="#f44336")
            self.status_label.config(text=f"Automatikmodus läuft von {start} bis {ende}", fg="green")

        else:
            if self.auto_instanz:
                self.auto_instanz.beenden()
                self.gui_controller.home_page.stop_tracking()
            self.running = False
            self.toggle_btn.config(text="Start", bg="#4CAF50")
            self.status_label.config(text="Automatikmodus gestoppt", fg="blue")

        # Status speichern nach jeder Änderung
        if self.auto_instanz:
            self.auto_instanz.status_speichern()




    def start_tracking_automatisch(self):
        self.gui_controller.active_pages["HomePage"].on_start_button_click()

    def stop_tracking_automatisch(self):
        self.gui_controller.active_pages["HomePage"].on_stop_button_click()



