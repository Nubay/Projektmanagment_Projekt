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

#Hervorhebung besonderer Orte
class AufenthaltsortErkennung:
    def __init__(self):
        self.letzter_ort = None
        self.letzte_zeit = None 
        self.aufenthaltsbeginn = None
    
    def entfernung_berechnen(self, coord1, coord2):
        from math import radians,sin,cos,sqrt,atan2
        R = 6371000 #Meter
        lat1, lon1 = radians(coord1[0]),radians(coord1[1])
        lat2, lon2 = radians(coord2[0]),radians(coord2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
    
    def verarbeite_datenpunkt(self,lat,lon,timestamp):
        import os, json
        from datetime import datetime, timedelta

        aktuelle_position = (lat,lon)
        zeitpunkt = datetime.fromisoformat(timestamp)

        if self.letzter_ort is None :
            self.letzter_ort = aktuelle_position 
            self.aufenthaltsbeginn = zeitpunkt 
            return 
        
        distanz = self.entfernung_berechnen(self.letzter_ort,aktuelle_position)

        if distanz < 30:
            if zeitpunkt -self.aufenthaltsbeginn >= timedelta(minutes=15):
                daten = {
                     "lat": self.letzter_ort[0],
                    "lon": self.letzter_ort[1],
                    "von": self.aufenthaltsbeginn.isoformat(),
                    "bis": zeitpunkt.isoformat(),
                    "name": None,
                    "farbe": "braun"

                }

                #pfad = os.path.join("Model", "Aufenthaltsorte")
                #os.makedirs(pfad, exist_ok=True)
                #datei = os.path.join(pfad, f"{zeitpunkt.date()}.json")

                #if os.path.exists(datei):
                #    with open(datei, "r", encoding="utf-8") as f:
                #        vorhandene = json.load(f)
                #else:
                #    vorhandene = []

                #vorhandene.append(daten)
                #with open(datei, "w", encoding="utf-8") as f:
                #    json.dump(vorhandene, f, indent=2, ensure_ascii=False)

                # Zurücksetzen, damit nicht mehrfach gespeichert wird
                self.aufenthaltsbeginn = zeitpunkt
        else:
            self.letzter_ort = aktuelle_position
            self.aufenthaltsbeginn = zeitpunkt


class GPSBackendSignalMessung :
    def __init__(self, controller):
        self.stoppe_messung = False 
        # self.session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        self.daten = []
        self.controller = controller
        self.aufenthaltserkenner = AufenthaltsortErkennung()


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

            self.aufenthaltserkenner.verarbeite_datenpunkt(lat, lon, timestamp)



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


