import tkinter as tk
from tkinter import *
from View.Components.buttons import create_buttons, toggle_buttons
from Model.evaluation import GPSBackendSignalMessung
import threading
from Controller.controller import GPSController
from View.settings_page import SettingsPage

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.gps_controller = GPSController(self)
        self.root_controller = controller
        self.evaluation = GPSBackendSignalMessung(self.gps_controller)
        self.gui_controller = controller
        # Aufteilung der Seite
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)



        # Linker Bereich
        left_frame = tk.Frame(self, bg="white")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)

        label = Label(left_frame, text="Route", font=("Courier", 24))
        label.grid(row=0, column=0, sticky="nsew", padx=5)

        self.textfield = Text(left_frame, state="disabled", font=("Courier", 13))
        self.textfield.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Quit-Button
        quit_button = tk.Button(self, text="Quit", width=10, height=2, bg="red", fg="white", command=self.root_controller.destroy)
        quit_button.place(x=10, y=10)

        # Rechter Bereich (Buttons)
        button_frame = tk.Frame(self, bg="lightgray")
        button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
        button_frame.columnconfigure(0, weight=1)

        # Buttons erzeugen
        buttons = create_buttons(button_frame)

        # "Einstellungen"-Button 
        buttons[0].config(command=self.öffne_einstellungen)

        # "Start"-Button 
        buttons[-1].config(command=lambda: self.start_stop_action(buttons[-1]))

        # Alle Buttons anzeigen
        for i, btn in enumerate(buttons):
            btn.grid(row=i, column=0, sticky="nsew", padx=10, pady=5)

    def öffne_einstellungen(self):
        fenster = tk.Toplevel(self)
        fenster.title("Einstellungen")
        fenster.state("zoomed")       # Große Fläche
        fenster.resizable(False, False)
        seite = SettingsPage(fenster)
        seite.pack(expand=True, fill="both")

    def start_stop_action(self, button):
        toggle_buttons(button)
        if button["text"] == "Stop":
            self.evaluation.stoppe_messung = False
            threading.Thread(target=self.evaluation.StartMessung, daemon=True).start()
        else:
            self.evaluation.stoppen()

    def show_gps_data(self, data):
        self.textfield.config(state="normal")
        self.textfield.insert("end", data + "\n")
        self.textfield.see("end")
        self.textfield.config(state="disabled")

        

        