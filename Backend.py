# Hinweis: Importfehler hier nur auf Windows
# funktioniert aber auf dem Raspberry Pi nach Installation von 'python3-gps'
#(sudo apt install gpsd gpsd-clients python3-gps)

from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE 
import time
from datetime import datetime 

class GPSBackendSignalMessung :
    def __init__(self):
        self.stoppe_messung = False 
        self.session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        self.daten = []

    def empfange_gps_daten(self):
        while True:
            report = self.session.next()
            if report['class'] == 'TPV':
                lat = getattr(report, 'lat', None)
                lon = getattr(report, 'lon', None)
                time_gps = getattr(report, 'time', None)
                if lat is not None and lon is not None:
                    return (lat, lon , time_gps)
                
    def starte_messung(self):
        while not self.stoppe_messung:
            lat, lon, time_gps = self.empfange_gps_daten()
            timestamp = datetime.now().isoformat()


            self.daten.append({
                "zeitpunkt": timestamp,
                "latitude": lat,
                "longitude": lon,
                "time_gps": time_gps
            })

            time.sleep(30)


    def stoppen(self):
        self.stoppe_messung = True

    def gib_daten(self):
        return self.daten


