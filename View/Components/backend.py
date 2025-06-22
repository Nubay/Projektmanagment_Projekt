

class Automatikmodus(GPSBackendSignalMessung):

    def __init__(self,start,ende,controller=None):
            self.start= start #Alle Konstruktoren
            self.ende=ende  
            super().__init__(controller) 

    def empfange_gps_daten(self):
        import random
        lat = 80 + random.uniform(-0.0001, 0.0001)
        lon = 40 + random.uniform(-0.0001, 0.0001)
        time_gps = datetime.now().isoformat()
        return (lat, lon, time_gps)

    def starte_automatikmodus(self): #Funktion für den Automatikmodus
      if self.start == self.ende or self.start>self.ende:#überprüft ob die Eingabe des Users richtig ist
            raise ValueError("Start-und Endzeit dürfen nicht gleich sein")
      else: 
            super().StartMessung() # Das Tracking wird gestartet.Das Super ist eine Vererbung und startet den Prozess 
            print("Starte tracking",self.start,"bis",self.ende)
            super().starte_messung()
    def beende_automatikmodus(self): # Tracking wird beendet
        if self.start>= self.ende:
            super().stoppe_messung()

track1=Automatikmodus("13:00:01" , "13:00:01")
track1.starte_automatikmodus()
track1.beende_automatikmodus()


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


            