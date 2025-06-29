import tkinter as tk
from PIL import Image, ImageTk
import os
import math
import json


def deg2num_pixel(lat_deg, lon_deg, zoom, tile_size=256):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    x = (lon_deg + 180.0) / 360.0 * n * tile_size
    y = (1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n * tile_size
    return x, y


def latlon_to_pixel(lat, lon, zoom):
    n = 2.0 ** zoom
    x = (lon + 180.0) / 360.0 * n * 256
    y = (1.0 - math.log(math.tan(math.pi / 4 + lat * math.pi / 180.0 / 2)) / math.pi) / 2.0 * n * 256
    return x, y


class MapWidget(tk.Canvas):
    def __init__(self, parent, start_lat, start_lon, zoom=14, tile_size=256, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.tile_size = tile_size
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.zoom = zoom
        self.marker_list = []
        self.zeige_besondere_orte = True
        self.im_besonderen_ort = False
        self._tile_images = []

        self.bind("<Configure>", self.on_resize)
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)
        self.bind("<MouseWheel>", self.do_zoom)
        self.bind("<Button-4>", self.do_zoom)
        self.bind("<Button-5>", self.do_zoom)

        self.drag_start_x = None
        self.drag_start_y = None

        self.set_view(start_lat, start_lon)

    def set_view(self, lat, lon):
        self.tile_x_float, self.tile_y_float = deg2num_pixel(lat, lon, self.zoom, self.tile_size)
        self.tile_x = int(self.tile_x_float // self.tile_size)
        self.tile_y = int(self.tile_y_float // self.tile_size)
        self.offset_x = int(self.tile_x_float % self.tile_size) * -1
        self.offset_y = int(self.tile_y_float % self.tile_size) * -1
        self.draw_tiles()

    def on_resize(self, event):
        self.draw_tiles()

    def draw_tiles(self):
        self.delete("tile")
        self._tile_images.clear()

        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 1 or height <= 1:
            return

        self.tiles_across = width // self.tile_size + 2
        self.tiles_down = height // self.tile_size + 2

        for row in range(self.tiles_down):
            for col in range(self.tiles_across):
                tile_x = self.tile_x + col
                tile_y = self.tile_y + row
                TILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "tiles"))
                tile_path = os.path.join(TILE_DIR, str(self.zoom), str(tile_x), f"{tile_y}.png")

                x_pos = col * self.tile_size + self.offset_x
                y_pos = row * self.tile_size + self.offset_y

                if os.path.exists(tile_path):
                    img = Image.open(tile_path)
                    tile_img = ImageTk.PhotoImage(img)
                    self.create_image(x_pos, y_pos, image=tile_img, anchor="nw", tags="tile")
                    self._tile_images.append(tile_img)
                else:
                    self.create_rectangle(x_pos, y_pos, x_pos + self.tile_size, y_pos + self.tile_size,
                                          fill="gray", tags="tile")

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
            self.zoom = min(max(self.zoom + (1 if event.delta > 0 else -1), 14), 16)
        elif event.num == 4:
            self.zoom = min(self.zoom + 1, 16)
        elif event.num == 5:
            self.zoom = max(self.zoom - 1, 14)

        if self.zoom != old_zoom:
            canvas_x, canvas_y = self.winfo_width() // 2, self.winfo_height() // 2
            lat, lon = self.canvas_to_latlon(canvas_x, canvas_y)
            self.set_view(lat, lon)

    def canvas_to_latlon(self, x, y):
        pixel_x = self.tile_x * self.tile_size + x - self.offset_x
        pixel_y = self.tile_y * self.tile_size + y - self.offset_y
        n = 2.0 ** self.zoom
        lon = pixel_x / (n * self.tile_size) * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * pixel_y / (n * self.tile_size))))
        lat = math.degrees(lat_rad)
        return lat, lon

    def update_overlay(self):
        self.delete("overlay")
        for lat, lon, color in self.marker_list:
            self._draw_marker(lat, lon, color)

    def latlon_to_canvas_coords(self, lat, lon):
        pixel_x_global, pixel_y_global = deg2num_pixel(lat, lon, self.zoom, self.tile_size)
        origin_x_global = self.tile_x * self.tile_size - self.offset_x
        origin_y_global = self.tile_y * self.tile_size - self.offset_y
        return pixel_x_global - origin_x_global, pixel_y_global - origin_y_global

    def _draw_marker(self, lat, lon, color="blue"):
        x, y = self.latlon_to_canvas_coords(lat, lon)
        r = 5
        self.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black", width=1, tag="overlay")

    def set_marker(self, lat, lon, color="blue"):
        self.marker_list.append((lat, lon, color))
        self._draw_marker(lat, lon, color)
