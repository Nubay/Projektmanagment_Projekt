import tkinter as tk
import os
import json


class Routen_Anzeigen_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Grid-Layout wie bei den anderen Seiten
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Zurück-Button oben links
        back_button = tk.Button(
            self,
            text="← Zurück",
            font=("Arial", 16, "bold"),
            bg="#d3d3d3",
            command=lambda: self.controller.show_page("RoutenPage")
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Textfeld, um Routen-Daten anzuzeigen
        self.textfield = tk.Text(self, state="disabled", font=("Courier", 13))
        self.textfield.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def zeige_route(self, route_text):
        self.textfield.config(state="normal")
        self.textfield.delete("1.0", "end")
        self.textfield.insert("end", route_text)
        self.textfield.config(state="disabled")