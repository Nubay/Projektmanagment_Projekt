import time
import random
import socket

HOST = 'localhost'
PORT = 5000

def generate_nmea_sentence(lat, lon):
    lat_deg = int(lat)
    lat_min = (lat - lat_deg) * 60
    lat_dir = 'N' if lat >= 0 else 'S'

    lon_deg = int(lon)
    lon_min = (lon - lon_deg) * 60
    lon_dir = 'E' if lon >= 0 else 'W'

    nmea = f"$GPGGA,123519,{abs(lat_deg):02d}{abs(lat_min):06.3f},{lat_dir}," \
           f"{abs(lon_deg):03d}{abs(lon_min):06.3f},{lon_dir},1,08,0.9,545.4,M,46.9,M,,*47"
    return nmea + "\r\n"

def main():
    lat = 48.1173
    lon = 11.5167

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print("[INFO] Warte auf Verbindung von socat...")
        conn, addr = server_socket.accept()
        with conn:
            print(f"[INFO] Verbunden mit socat von {addr}")
            while True:
                lat += random.uniform(-0.01, 0.01)
                lon += random.uniform(-0.01, 0.01)
                sentence = generate_nmea_sentence(lat, lon)
                conn.sendall((sentence + "\n").encode())
                print(f"[DEBUG] Gesendet: {sentence}")
                time.sleep(1)

if __name__ == '__main__':
    main()
