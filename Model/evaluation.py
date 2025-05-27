# Hinweis: Importfehler hier nur auf Windows
# funktioniert aber auf dem Raspberry Pi nach Installation von 'python3-gps'
#(sudo apt install gpsd gpsd-clients python3-gps)

# from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE 
import time
from datetime import datetime 

import json
import os
from datetime import datetime
from typing import List, Tuple
from Controller.controller import GPSController



def berechne_gps_mittelwert(gps_daten: List[Tuple[float, float]]) -> Tuple[float, float]:
    if not gps_daten:
        raise ValueError("Die Liste ist nicht gefüllt.")
    summe_breite = sum(koord[0] for koord in gps_daten)
    summe_laenge = sum(koord[1] for koord in gps_daten)
    anzahl = len(gps_daten)

    mittelwert_breite = summe_breite / anzahl
    mittelwert_laenge = summe_laenge / anzahl


    return (mittelwert_breite, mittelwert_laenge)


def save_value_daily(value, directory=os.path.join("Model", "JsonDateinTage")):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(directory, f"{today}.json")
    
    os.makedirs(directory, exist_ok=True)
    
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(value)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



class GPSBackendSignalMessung :
    def __init__(self, controller):
        self.stoppe_messung = False 
        # self.session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        self.daten = []
        self.controller = controller


        #GPS Daten mit Modul
    # def empfange_gps_daten(self):
    #     while True:
    #         report = self.session.next()
    #         if report['class'] == 'TPV':
    #             lat = getattr(report, 'lat', None)
    #             lon = getattr(report, 'lon', None)
    #             time_gps = getattr(report, 'time', None)
    #             if lat is not None and lon is not None:
    #                 return (lat, lon , time_gps)
                


        # Dummy GPS Daten
    def empfange_gps_daten(self):
        import random
        lat = 80 + random.uniform(-10.5, 10.5)
        lon = 40 + random.uniform(-5.5, 5.5)
        time_gps = datetime.now().isoformat()
        return (lat, lon, time_gps)



    def starte_messung(self):
        messungen = []
        while not self.stoppe_messung:
            lat, lon, time_gps = self.empfange_gps_daten()
            timestamp = datetime.now().isoformat()


            self.daten.append({
                "lat": lat,
                "lon": lon,
                "time_gps": time_gps,
                "timestamp": timestamp
            })


            messungen.append((lat, lon))
            if len(messungen) == 2:
                return messungen

            time.sleep(2)


    def stoppen(self):
        self.stoppe_messung = True

    def gib_daten(self):
        return self.daten

    def StartMessung(self):
        while 1:
            gps_daten = self.starte_messung()
            self.controller.submit_data(berechne_gps_mittelwert(gps_daten))
            save_value_daily(berechne_gps_mittelwert(gps_daten))

