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
import platform
from pathlib import Path



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


    @staticmethod
    def exportiere_gruppiert_nach_dateiname(export_dateiname='vereint.json'):
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        quellordner = os.path.join(base_dir, 'JsonDateinTage')
        gesammelte_daten = {}

        # 1. Alle JSON-Dateien einlesen und unter ihrem Dateinamen speichern
        for dateiname in os.listdir(quellordner):
            if dateiname.endswith('.json'):
                pfad = os.path.join(quellordner, dateiname)
                with open(pfad, 'r', encoding='utf-8') as f:
                    try:
                        daten = json.load(f)
                        if isinstance(daten, list):
                            gesammelte_daten[dateiname] = daten
                    except json.JSONDecodeError:
                        print(f"Fehler beim Laden von {pfad}")

        # 2. USB-Stick-Pfad suchen
        usb_pfad = finde_usb_stick_pfad()
        if not usb_pfad:
            print("Kein USB-Stick gefunden.")
            return

        export_pfad = os.path.join(usb_pfad, export_dateiname)

        # 3. Exportieren
        with open(export_pfad, 'w', encoding='utf-8') as f:
            json.dump(gesammelte_daten, f, indent=2)
        print(f"Daten erfolgreich exportiert nach: {export_pfad}")


def finde_usb_stick_pfad():
    system = platform.system()
    mögliche_pfade = []

    if system == 'Windows':
        for laufwerk in ['D:', 'E:', 'F:', 'G:', 'H:']:
            if os.path.exists(laufwerk):
                mögliche_pfade.append(laufwerk)
    else:
        media_root = '/media/' + os.getlogin()
        if os.path.exists(media_root):
            mögliche_pfade = [os.path.join(media_root, d) for d in os.listdir(media_root)]

    for pfad in mögliche_pfade:
        if os.path.isdir(pfad) and os.access(pfad, os.W_OK):
            return pfad

    return None

