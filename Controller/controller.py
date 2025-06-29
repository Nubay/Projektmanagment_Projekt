from typing import Tuple

class GPSController:
    def __init__(self, homepage):
        self.homepage = homepage

    def submit_data(self, daten: Tuple[float, float]):
        lat, lon = daten
        def update_ui():
            self.homepage.map_widget.set_marker(lat, lon)
            
        self.homepage.after(0, update_ui)

    def show_password_check_page(self, zielseite):
        self.password_check_page.set_weiterleitungsziel(zielseite)
        self.show_page("PasswordCheckPage")


