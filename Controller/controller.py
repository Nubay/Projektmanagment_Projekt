from typing import Tuple
from View.homepage import HomePage

class GPSController:
    def __init__(self):
        self.homepage = HomePage(self)

    
    def submit_data(self, daten: Tuple[float, float]):
        gps_data = daten
        self.homepage.show_gps_data(gps_data)

