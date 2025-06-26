import tkinter as tk
from PIL import Image, ImageTk
import os
import math
from math import log, tan, pi, atan, sinh
import json


def deg2num_pixel(lat_deg, lon_deg, zoom, tile_size=256):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    x = (lon_deg + 180.0) / 360.0 * n * tile_size
    y = (1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n * tile_size
    return x, y


def deg2num_tile(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile



def latlon_to_pixel(lat, lon, zoom):
    n = 2.0 ** zoom
    x = (lon + 180.0) / 360.0 * n * 256
    y = (1.0 - log(tan(pi / 4 + lat * pi / 180.0 / 2)) / pi) / 2.0 * n * 256
    return x, y



class MapWidget(tk.Canvas):
    def __init__(self, parent, width, height, start_lat, start_lon, zoom=14, tile_size=256, *args, **kwargs):
        super().__init__(parent, width=width, height=height, *args, **kwargs)

        self.marker_list = []
        self.zeige_besondere_orte = True
        self.im_besonderen_ort = False



        self.tile_size = tile_size  # zuerst setzen!

        self.tile_x_float, self.tile_y_float = deg2num_pixel(start_lat, start_lon, zoom, self.tile_size)
        self.tile_x = int(self.tile_x_float // self.tile_size)
        self.tile_y = int(self.tile_y_float // self.tile_size)

        self.offset_x = int(self.tile_x_float % self.tile_size) * -1
        self.offset_y = int(self.tile_y_float % self.tile_size) * -1

        self.tiles_across = width // self.tile_size + 1
        self.tiles_down = height // self.tile_size + 1
        self.zoom = zoom
        self.start_lat = start_lat
        self.start_lon = start_lon


        self._tile_images = []

        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)
        self.bind("<MouseWheel>", self.do_zoom)  
        self.bind("<Button-4>", self.do_zoom)    
        self.bind("<Button-5>", self.do_zoom)    

        self.drag_start_x = None
        self.drag_start_y = None

        self.draw_tiles()

    def draw_tiles(self):
        self.delete("tile")
        self._tile_images.clear()


        for row in range(self.tiles_down):
            for col in range(self.tiles_across):
                tile_x = self.tile_x + col
                tile_y = self.tile_y + row
                TILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "tiles"))
                tile_path = os.path.join(TILE_DIR, str(self.zoom), str(tile_x), f"{tile_y}.png")


                if os.path.exists(tile_path):
                    img = Image.open(tile_path)
                    tile_img = ImageTk.PhotoImage(img)
                    x_pos = col * self.tile_size + self.offset_x
                    y_pos = row * self.tile_size + self.offset_y
                    self.create_image(x_pos, y_pos, image=tile_img, anchor="nw")
                    self._tile_images.append(tile_img)
                else:
                    x_pos = col * self.tile_size + self.offset_x
                    y_pos = row * self.tile_size + self.offset_y
                    self.create_rectangle(x_pos, y_pos, x_pos+self.tile_size, y_pos+self.tile_size, fill="gray")

        self.update_overlay()


    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        self.offset_x += dx
        self.offset_y += dy

        while self.offset_x > 0:
            self.tile_x -= 1
            self.offset_x -= self.tile_size
        while self.offset_x < -self.tile_size:
            self.tile_x += 1
            self.offset_x += self.tile_size

        while self.offset_y > 0:
            self.tile_y -= 1
            self.offset_y -= self.tile_size
        while self.offset_y < -self.tile_size:
            self.tile_y += 1
            self.offset_y += self.tile_size

        self.drag_start_x = event.x
        self.drag_start_y = event.y

        self.draw_tiles()

    def do_zoom(self, event):
        old_zoom = self.zoom
        if hasattr(event, "delta"):
            if event.delta > 0:
                self.zoom = min(self.zoom + 1, 16)
            else:
                self.zoom = max(self.zoom - 1, 14)
        else:
            if event.num == 4:
                self.zoom = min(self.zoom + 1, 16)
            elif event.num == 5:
                self.zoom = max(self.zoom - 1, 14)

        if self.zoom != old_zoom:
            # Rechne aktuelle Kartenposition (lat/lon) aus
            pixel_x, pixel_y = self.tile_x * self.tile_size + abs(self.offset_x), self.tile_y * self.tile_size + abs(self.offset_y)
            n = 2.0 ** old_zoom
            lon = pixel_x / (n * self.tile_size) * 360.0 - 180.0
            lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * pixel_y / (n * self.tile_size))))
            lat = math.degrees(lat_rad)

            # Jetzt neue Tile-Position berechnen
            self.tile_x_float, self.tile_y_float = deg2num_pixel(lat, lon, self.zoom, self.tile_size)
            self.tile_x = int(self.tile_x_float // self.tile_size)
            self.tile_y = int(self.tile_y_float // self.tile_size)
            self.offset_x = int(self.tile_x_float % self.tile_size) * -1
            self.offset_y = int(self.tile_y_float % self.tile_size) * -1

            self.draw_tiles()


    def latlon_to_canvas_coords(self, lat, lon):
        pixel_x_global, pixel_y_global = deg2num_pixel(lat, lon, self.zoom, self.tile_size)
        origin_x_global = self.tile_x * self.tile_size - self.offset_x
        origin_y_global = self.tile_y * self.tile_size - self.offset_y

            # Pixel innerhalb des Tiles
        canvas_x = pixel_x_global - origin_x_global
        canvas_y = pixel_y_global - origin_y_global

        return canvas_x, canvas_y
    
    def entfernung_berechnen(self, coord1, coord2):
        from math import radians, sin, cos, sqrt, atan2
        R = 6371000  # Erd-Radius in Metern
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    

    def update_overlay(self):
        self.delete("overlay")
        for lat, lon, color in self.marker_list:
            self._draw_marker(lat, lon, color)

        if len(self.marker_list) > 1:
            points = [self.latlon_to_canvas_coords(lat, lon) for lat, lon, _ in self.marker_list]
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                self.create_line(x1, y1, x2, y2, fill="red", width=2, tag="overlay")






    def set_route_line(self, punktliste):
        if len(punktliste) < 2:
            return

        canvas_coords = []

        for lat, lon in punktliste:
            besondere_position = self.ist_in_der_naehe_eines_besonderen_orts(lat, lon)
            if besondere_position:
                lat, lon = besondere_position  # <- Punkt auf gespeicherten Ort setzen
                color = "red"
            else:
                color = "blue"
            
            x, y = self.latlon_to_canvas_coords(lat, lon)
            canvas_coords.append((x, y, color))

        for i in range(len(canvas_coords) - 1):
            x1, y1, color1 = canvas_coords[i]
            x2, y2, color2 = canvas_coords[i + 1]

            # Wenn beide Punkte die gleiche Farbe haben, verwende diese
            if color1 == color2:
                line_color = color1
            else:
                line_color = "purple"  # Mischfarbe, wenn ein Übergang passiert (optional)

            self.create_line(x1, y1, x2, y2, fill=line_color, width=3, tag="overlay")




    def _draw_marker(self, lat, lon, color="blue"):
        x, y = self.latlon_to_canvas_coords(lat, lon)
        radius = 5
        self.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=color, outline="black", width=1, tag="overlay"
        )


    
    def set_marker(self, lat, lon, color=None):
        if color is None:
            nahe_ort = self.ist_in_der_naehe_eines_besonderen_orts(lat, lon)
            if nahe_ort:
                lat, lon = nahe_ort  # Marker direkt auf bekannten Ort setzen!
                color = "red"
            else:
                color = "blue"
        
        self.marker_list.append((lat, lon, color))
        self._draw_marker(lat, lon, color)





    def zeichne_besondere_orte(self):
        pfad = os.path.join("Model", "JSONBesondereOrte", "besondere_orte.json")
        if not os.path.exists(pfad):
            return

        with open(pfad, "r", encoding="utf-8") as f:
            daten = json.load(f)

        for ort in daten:
            lat = ort["lat"]
            lon = ort["lon"]
            farbe = ort.get("farbe", "red")

            x, y = self.latlon_to_canvas_coords(lat, lon)

            r = 5
            self.create_oval(
                x - r, y - r, x + r, y + r,
                fill=farbe, outline="black", width=1, tag="overlay"
            )


    def ist_in_der_naehe_eines_besonderen_orts(self, lat, lon, radius=50):
        pfad = os.path.join("Model", "JSONBesondereOrte", "besondere_orte.json")
        if not os.path.exists(pfad):
            return None

        with open(pfad, "r", encoding="utf-8") as f:
            try:
                daten = json.load(f)
            except json.JSONDecodeError:
                return None

        for ort in daten:
            ort_lat = ort.get("lat")
            ort_lon = ort.get("lon")
            if ort_lat is not None and ort_lon is not None:
                distanz = self.entfernung_berechnen((lat, lon), (ort_lat, ort_lon))
                if distanz <= radius:
                    return ort_lat, ort_lon  # <-- Änderung: gibt Koordinaten zurück

        return None











