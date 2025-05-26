from typing import Tuple

class GPSController:
    def __init__(self, homepage):
        self.homepage = homepage

    def submit_data(self, daten: Tuple[float, float]):
        def update_ui():
            self.homepage.show_gps_data(f"Längengrad: {daten[0]:.5f}, Breitengrad: {daten[1]:.5f}")
        self.homepage.after(0, update_ui)

