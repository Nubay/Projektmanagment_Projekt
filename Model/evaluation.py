import json
import os
from datetime import datetime
from typing import List, Tuple


def berechne_gps_mittelwert(gps_daten: List[Tuple[float, float]]) -> Tuple[float, float]:
    if not gps_daten:
        raise ValueError("Die Liste ist nicht gefüllt.")
    summe_breite = sum(koord[0] for koord in gps_daten)
    summe_laenge = sum(koord[1] for koord in gps_daten)
    anzahl = len(gps_daten)

    mittelwert_breite = summe_breite / anzahl
    mittelwert_laenge = summe_laenge / anzahl


    return (mittelwert_breite, mittelwert_laenge)


def save_value_daily(value, directory="JsonDateinTage"):
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
gps_daten = [(2.5200, 13.4050), (84.8566, 2.3522), (55.1657, 180.4515)]

save_value_daily(berechne_gps_mittelwert(gps_daten))