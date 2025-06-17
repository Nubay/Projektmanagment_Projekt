import tkinter as tk
import os
import json


class RoutenPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        

        # Grid-Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


        # Back Button
        back_button = tk.Button(self, text="← Zurück", font=("Arial", 16, "bold"), bg="#d3d3d3",
                                command=lambda: self.controller.show_page("HomePage"))
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)


        # Scrollbar für Routen-Buttons
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.routes_button_frame = tk.Frame(self.canvas)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.routes_button_frame, anchor="nw")

        self.routes_button_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))


        # Frame-Breite an Canvas anpassen
        self.canvas.bind("<Configure>", lambda e: 
        self.canvas.itemconfig(self.canvas_window, width=e.width))


        self.route_buttons = []

        self.update_route_list()



    def add_route_button(self, route_name, command):
        btn = tk.Button(self.routes_button_frame,
                        text=route_name,
                        font=("Arial", 18, "bold"),
                        bg="#a0a0a0",
                        activebackground="#808080",
                        fg="white",
                        pady=20,
                        command=command)
        btn.pack(side="top", fill="x", pady=5, expand=True)
        
        self.route_buttons.insert(0, btn)



    def lade_alle_routen_und_aktualisiere_buttons(self):
        directory = os.path.join("Model", "JsonDateinTage")
        dateien = [f for f in os.listdir(directory) if f.endswith(".json")]
        
        # Clear alte Buttons zuerst
        for btn in self.route_buttons:
            btn.destroy()
        self.route_buttons.clear()

        for datei in sorted(dateien, reverse=True):
            pfad = os.path.join(directory, datei)
            try:
                with open(pfad, "r", encoding="utf-8") as f:
                    daten = json.load(f)
                    # Beispiel: Name aus Dateiname oder Inhalt ziehen
                    route_name = datei.replace(".json", "")
                    # Button hinzufügen
                    self.add_route_button(route_name, lambda rn=route_name: print(f"Route {rn} ausgewählt"))
            except Exception as e:
                print(f"Fehler beim Laden von {datei}: {e}")



    def update_route_list(self):
        self.lade_alle_routen_und_aktualisiere_buttons()
        