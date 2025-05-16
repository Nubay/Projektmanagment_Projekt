class GPSController:
    def __init__(self, homepage):
        self.homepage = homepage

    
    def submit_data(self):
        gps_data = "520N, 320E"
        self.homepage.show_gps_data(gps_data)


