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
import threading
import time
import time as time_module
from View.Components.benachrichtigung import NotificationDialog



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

    # Ordner erstellen, falls nicht vorhanden
    os.makedirs(directory, exist_ok=True)

    # Liste der JSON-Dateien im Verzeichnis holen
    json_files = [f for f in os.listdir(directory) if f.endswith(".json")]

    # Wenn mehr als oder gleich 100 Dateien vorhanden sind, die älteste löschen
    if len(json_files) >= 100:
        full_paths = [os.path.join(directory, f) for f in json_files]
        oldest_file = min(full_paths, key=os.path.getctime)
        os.remove(oldest_file)

    # Bestehende Datei laden oder leere Liste erstellen
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Wert hinzufügen und Datei speichern
    data.append(value)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



#Hervorhebung besonderer Orte
class AufenthaltsortErkennung:
    def __init__(self):
        self.letzter_ort = None
        self.letzte_zeit = None 
        self.aufenthaltsbeginn = None

        #Ordner und Datei für besondere Orte dauerhaft vorbereiten
        pfad = os.path.join("Model", "JSONBesondereOrte")
        os.makedirs(pfad,exist_ok=True)
        datei = os.path.join(pfad ,"besondere_orte.json")
        if not os.path.exists(datei):
            with open(datei, "w", encoding="utf-8") as f:
                json.dump([], indent =2 , ensure_ascii=False)
    
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
        

        if distanz < 50:
            
            if zeitpunkt -self.aufenthaltsbeginn >= timedelta(minutes=15):
                
                daten = {
                    "lat": self.letzter_ort[0],
                    "lon": self.letzter_ort[1],
                    "name": "Neuer Ort",
                    "farbe": "red"

                }

                pfad = os.path.join("Model", "JSONBesondereOrte")
                
                datei = os.path.join(pfad,"besondere_orte.json")

                if os.path.exists(datei):
                    with open(datei, "r", encoding="utf-8") as f:
                        try:
                             daten_liste = json.load(f)
                        except json.JSONDecodeError:
                             daten_liste = []

                else:
                     daten_liste = []

                bereits_vorhanden = any(
                self.entfernung_berechnen((ort["lat"], ort["lon"]), self.letzter_ort) < 5
                for ort in daten_liste
                )

                if not bereits_vorhanden:
                 #Besonderer Ort hinzufügen 
                    daten_liste.append(daten)
                    with open (datei, "w", encoding="utf-8") as f:
                        json.dump(daten_liste, f, ensure_ascii=False, indent=2)    

                   
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
    #                 last_lat = lat 
    #                 last_lon = lon
    #                 last_time = time_gps
    #                 return (lat, lon , time_gps)
    #             else: 
    #                 self.controller.submit_data('SIGNALVERLUST! Letzter Standort :')
    #                 return(last_lat, last_lon, last_time)



        # Dummy GPS Daten
    def empfange_gps_daten(self):
        import random
        lat = 50.58815615354921 + random.uniform(-0.00001, 0.00001)
        lon = 7.2047427345133 + random.uniform(-0.00001, 0.00001)
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
            time.sleep(4)
            self.controller.submit_data(berechne_gps_mittelwert(gps_daten))
            save_value_daily(berechne_gps_mittelwert(gps_daten))



    @staticmethod
    def exportiere_gruppiert_nach_dateiname(parent, export_dateiname='vereint.json'):
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
                        NotificationDialog(parent, message="Fehler beim Laden!")
                        print(f"Fehler beim Laden von {pfad}")

        # 2. USB-Stick-Pfad suchen
        usb_pfad = finde_usb_stick_pfad()
        if not usb_pfad:
            print("Kein USB-Stick gefunden.")
            NotificationDialog(parent, message="Kein USB-Stick gefunden!")
            return

        export_pfad = os.path.join(usb_pfad, export_dateiname)

        # 3. Exportieren
        with open(export_pfad, 'w', encoding='utf-8') as f:
            json.dump(gesammelte_daten, f, indent=2)
        NotificationDialog(parent, message="Daten erfolgreich exportiert!")
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



def lade_und_verarbeite_gps_daten():
    directory = os.path.join("Model", "JsonDateinTage")
    dateien = [f for f in os.listdir(directory) if f.endswith(".json")]

    routes = []

    for datei in sorted(dateien, reverse=True):
        route_name = datei.replace(".json", "")
        pfad = os.path.join(directory, datei)

        gps_punkte = []
        try:
            with open(pfad, "r", encoding="utf-8") as f:
                daten = json.load(f)
            for eintrag in daten:
                if isinstance(eintrag, list) and len(eintrag) == 2:
                    lat, lon = eintrag 
                    gps_punkte.append((lat, lon))  # wir drehen sie hier um
        except Exception as e:
            print(f"Fehler beim Laden der Route {route_name}: {e}")
            continue  # diese Route überspringen, wenn fehlerhaft

        routes.append((route_name, gps_punkte))

    return routes


    
class Automatikmodus:
    STATUS_DATEI = "automatik_status.json"

    def __init__(self, start_time_str, end_time_str, home_page, automatik_page):
        self.start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        self.end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
        self.home_page = home_page
        self.automatik_page = automatik_page
        self.running = False
        self.started = False
        

    def status_speichern(self):
        status = {
            "running": self.running,
            "started": self.started,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
        }
        ordner_pfad = "Model/JSONAutomatikmodus"
        os.makedirs(ordner_pfad, exist_ok=True)
        datei_pfad = os.path.join(ordner_pfad, "status.json")

        with open(datei_pfad, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2)

    def status_laden(self):
        if os.path.exists(self.STATUS_DATEI):
            with open(self.STATUS_DATEI, "r", encoding="utf-8") as f:
                status = json.load(f)
                self.running = status.get("running", False)
                self.started = status.get("started", False)
                self.start_time = datetime.strptime(status.get("start_time", "00:00:00"), "%H:%M:%S").time()
                self.end_time = datetime.strptime(status.get("end_time", "23:59:59"), "%H:%M:%S").time()
                return True
        return False


    def starten(self):
        self.running = True
        self.status_speichern()
        now = datetime.now().time()
        if self.start_time <= now < self.end_time:
            self.started = True
            self.automatik_page.start_tracking_automatisch()
        self._check_time()

    def beenden(self):
        self.running = False
        if self.started:
            self.home_page.automatisch_stop()
            self.started = False
        self.status_speichern()

    def _check_time(self):
        if not self.running:
            return

        now = datetime.now().time()

        if not self.started and self.start_time <= now < self.end_time:
            print("Automatikmodus: Startzeit erreicht, Tracking starten")
            self.started = True
            self.automatik_page.start_tracking_automatisch()

        elif self.started and now >= self.end_time:
            print("Automatikmodus: Endzeit erreicht, Tracking stoppen")
            self.started = False
            self.running = False
            self.automatik_page.stop_tracking_automatisch()
            return

        self.home_page.after(1000, self._check_time)



    


class Aufenthaltserkennung(AufenthaltsortErkennung):  
    def __init__(self, letzte_position, aktuelle_position, timestamp):
        super().__init__()
        self.letzte_position = letzte_position
        self.position = aktuelle_position
        self.timestamp = timestamp  # ISO-String oder datetime

    def vergleiche_punkte(self):
        entfernung = self.entfernung_berechnen(self.letzte_position, self.position)

        if entfernung < 50:
            # Simuliere Übergabe an Basisklasse, um zu prüfen, ob ein langer Aufenthalt vorliegt
            self.verarbeite_datenpunkt(self.position[0], self.position[1], self.timestamp)
        else:
            print("Person hat sich bewegt (mehr als 50m).")

