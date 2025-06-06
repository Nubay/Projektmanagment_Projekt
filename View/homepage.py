import tkinter as tk
from tkinter import *
from View.Components.buttons import create_buttons, toggle_buttons
from Model.evaluation import GPSBackendSignalMessung
import threading
from Controller.controller import GPSController

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = GPSController(self)
        self.evaluation = GPSBackendSignalMessung(self.controller)


        #Aufteilung Seite in 2
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        #Aufteilung Linke Seite
        left_frame = tk.Frame(self, bg="white")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)


        #Label + Textfeld
        label = Label(left_frame, text = "Route")
        label.config(font = ('Courier', 24))
        label.grid(row=0, column=0, sticky="nsew", padx=5)

        self.textfield = Text(left_frame, state="disabled", font=("Courier", 13))
        self.textfield.grid(row = 1, column = 0, sticky = "nsew", padx=5, pady = 5)


        # Quit-Button
        quit_button = tk.Button(self, text="Quit", width=10, height=2, bg="red", fg="white", command=controller.destroy)
        quit_button.place(x=10, y=10)



        #Aufteilung Rechte Seite
        #Buttons Rechts
        button_frame = tk.Frame(self, bg="lightgray")
        button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        for i in range(4):
            button_frame.rowconfigure(i, weight=1)
        button_frame.columnconfigure(0, weight=1)


        # Buttons erstellen
        buttons = create_buttons(button_frame)

        for i, btn in enumerate(buttons):
            btn.grid(row=i, column=0, sticky="nsew", padx=10, pady=5)


        # Start/Stop-Button
        start_stop_button = buttons[3]
        start_stop_button.config( 
            command=lambda: self.start_stop_action(start_stop_button)
        )

        
        #Exportieren/Button
        export_button = buttons[1]
        export_button.config(command=self.exportieren_action)

    
    def exportieren_action(self):
        self.evaluation.exportiere_gruppiert_nach_dateiname()



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
        

        