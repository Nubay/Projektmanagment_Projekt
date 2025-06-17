import tkinter as tk
import os


class StandortPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)


        # Back Button
        back_button = tk.Button(self, text="← Zurück", font=("Arial", 16, "bold"), bg="#d3d3d3",
                                command=lambda: self.controller.show_page("HomePage"))
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)


        # Canvas für Scrollbar
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.routes_button_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.routes_button_frame, anchor="nw")

        self.routes_button_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.canvas.bind("<Configure>", lambda e:
                         self.canvas.itemconfig(self.canvas_window, width=e.width))



