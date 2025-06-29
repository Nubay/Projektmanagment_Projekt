import tkinter as tk
from tkinter import *
from View.Components.buttons import create_buttons, toggle_buttons
from Model.evaluation import GPSBackendSignalMessung
import threading
from Controller.controller import GPSController
from View.Components.map import MapWidget
from View.Components.bestätigung import ConfirmationDialog





class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.gps_controller = GPSController(self)
        self.root_controller = controller
        self.evaluation = GPSBackendSignalMessung(self.gps_controller)
        self.gui_controller = controller
        self.running = False



        #Aufteilung Seite in 2
        self.columnconfigure(0, weight=9)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)



        # Linker Bereich
        left_frame = tk.Frame(self, bg="white")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
  

        self.map_widget = MapWidget(left_frame, 
                            start_lat=50.589, start_lon=7.206, zoom=14)
        self.map_widget.grid(row=1, column=0, sticky="nsew")
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)



        # self.textfield = Text(left_frame, state="disabled", font=("Courier", 13))
        # self.textfield.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        def quit_action():
            ConfirmationDialog(self, message="App wirklich beenden?", on_confirm=self.root_controller.destroy)


        # Quit-Button
        quit_button = tk.Button(self, text="Quit", width=10, height=2, bg="red", fg="white", command=quit_action)
        quit_button.place(x=10, y=10)


        # Rechter Bereich (Buttons)
        button_frame = tk.Frame(self, bg="lightgray")
        button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
        button_frame.columnconfigure(0, weight=1)

        # Buttons erzeugen
        buttons = create_buttons(button_frame)


        # "Start"-Button 
        buttons[-1].config(command=lambda: self.start_stop_action(buttons[-1]))

        # Alle Buttons anzeigen
        for i, btn in enumerate(buttons):
            btn.grid(row=i, column=0, sticky="nsew", padx=10, pady=5)


        # Start/Stop-Button als Instanzvariable speichern
        self.start_stop_button = buttons[4]
        self.start_stop_button.config(command=lambda: self.start_stop_action(self.start_stop_button))


        def oeffne_settings_mit_passwort():
            self.gui_controller.active_pages["PasswortPage"].set_weiterleitungsziel("SettingsPage")
            self.gui_controller.show_page("PasswortPage")
            


        # Einstellung Button
        einstellung_button = buttons[0]
        einstellung_button.config(command=oeffne_settings_mit_passwort)


        # Routen Button
        routen_button = buttons[1]
        routen_button.config(command=lambda: self.gui_controller.show_page("RoutenPage"))


        # Standort Button
        standort_button = buttons[2]
        standort_button.config(command=lambda: self.gui_controller.show_page("StandortPage"))

        
        #Exportieren/Button
        export_button = buttons[3]
        export_button.config(command=self.exportieren_action)

    
    def exportieren_action(self):
        self.evaluation.exportiere_gruppiert_nach_dateiname(self)



    def start_stop_action(self, button):
        toggle_buttons(button)
        if button["text"] == "Stop":
            self.evaluation.stoppe_messung = False
            print("Messung startet")
            threading.Thread(target=self.evaluation.StartMessung, daemon=True).start()
        else:
            self.evaluation.stoppen()


    def automatisch_start(self):
        if self.start_stop_button["text"] == "Start":
            self.start_stop_button.config(text="Stop", bg="orange")
            self.evaluation.stoppe_messung = False
            threading.Thread(target=self.evaluation.StartMessung, daemon=True).start()
    

    def automatisch_stop(self):
        if self.start_stop_button["text"] == "Stop":
            self.start_stop_button.config(text="Start", bg="green")
            self.evaluation.stoppen()



    def start_tracking(self):
        print("HomePage.start_tracking() aufgerufen")
        if not self.running:
            self.running = True
            self.automatisch_start()


    def stop_tracking(self):
        if self.running:
            self.running = False
            self.automatisch_stop()


    def on_start_button_click(self):
        self.start_tracking()


    def on_stop_button_click(self):
        self.stop_tracking()


    def show_gps_data(self, data):
        self.textfield.config(state="normal")
        self.textfield.insert("end", data + "\n")
        self.textfield.see("end")
        self.textfield.config(state="disabled")




        

        