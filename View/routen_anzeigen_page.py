import tkinter as tk
from View.Components.map import MapWidget
from Model.evaluation import berechne_gps_mittelwert



class Routen_Anzeigen_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Karte in eigenen Frame einbetten
        self.karten_frame = tk.Frame(self)
        self.karten_frame.pack(expand=True, fill="both")

        self.map_widget = MapWidget(self.karten_frame, width=7*256, height=5*256,
                                    start_lat=50.589, start_lon=7.206, zoom=14)
        self.map_widget.pack(expand=True, fill="both")

        # Zurück-Button oben links (bleibt sichtbar)
        back_button = tk.Button(
            self,
            text="← Zurück",
            font=("Arial", 16, "bold"),
            bg="#d3d3d3",
            command=lambda: self.controller.show_page("RoutenPage")
        )
        back_button.place(x=10, y=10)

    def zeige_route(self, gps_punkte):
        if not gps_punkte:
            return

        # Karte zentrieren auf Mittelwert
        mittel_lat, mittel_lon = berechne_gps_mittelwert(gps_punkte)

        # Alte Karte löschen
        self.map_widget.destroy()

        # Neue Karte erstellen
        self.map_widget = MapWidget(self.karten_frame, width=7*256, height=5*256,
                                    start_lat=mittel_lat, start_lon=mittel_lon, zoom=14)
        self.map_widget.pack(expand=True, fill="both")

        # Marker und Linie setzen
        for lat, lon in gps_punkte:
            self.map_widget.set_marker(lat, lon)

        self.map_widget.set_route_line(gps_punkte)


