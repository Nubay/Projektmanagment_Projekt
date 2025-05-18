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