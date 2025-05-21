from typing import Tuple


class GPSController:
    def __init__(self, homepage_ref):
        self.homepage = homepage_ref

    def submit_data(self, daten: Tuple[float, float]):
        self.homepage.show_gps_data(f"Lat: {daten[0]:.5f}, Lon: {daten[1]:.5f}")
        self.homepage.show_gps_data( '13345666432211 r')
