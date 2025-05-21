from typing import Tuple

class GPSController:
    def __init__(self, homepage):
        self.homepage = homepage

    
    def submit_data(self, daten: Tuple[float, float]):
        gps_data = daten
        self.homepage.show_gps_data(gps_data)
        gps_data2 = '12    34'
        self.homepage.show_gps_data(gps_data2)

