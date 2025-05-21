from typing import Tuple


class GPSController:
    
    def submit_data(self, daten: Tuple[float, float]):
        from View.homepage import HomePage
        self.homepage = HomePage(self)
        gps_data = daten
        self.homepage.show_gps_data(gps_data)

