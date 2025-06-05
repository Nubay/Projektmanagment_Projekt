# Funktion zum Speichern des Passworts in eine Textdatei
def speichere_passwort(passwort):
    with open("passwort.txt", "w", encoding="utf-8") as f:
        f.write(passwort)