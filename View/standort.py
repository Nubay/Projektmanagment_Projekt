import tkinter as tk
import subprocess


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

        # Beispiel-Daten
        self.besondere_orte = [
            {"name": "", "verweildauer": 18},
            {"name": "", "verweildauer": 26},
        ]

        self.refresh()

    def refresh(self):
        # Alte Einträge löschen
        for widget in self.routes_button_frame.winfo_children():
            widget.destroy()

        for idx, ort in enumerate(self.besondere_orte):
            ort_name = ort['name'] if ort['name'] else f"Besonderer Standort {idx + 1}"

            ort_frame = tk.Frame(self.routes_button_frame, bg="#a0a0a0", bd=1, relief="solid")
            ort_frame.pack(fill="x", padx=10, pady=5)

            label = tk.Label(ort_frame, text=f"{ort_name} ({ort['verweildauer']} min)",
                            anchor="w", font=("Arial", 20, "bold"), bg="#a0a0a0")
            label.pack(side="left", padx=10, pady=20, expand=True, fill="x")


            # Löschen-Button
            delete_btn = tk.Button(ort_frame, text="❌", font=("Arial", 14),
                                width=5, height=2,
                                command=lambda i=idx: self.loesche_ort(i))
            delete_btn.pack(side="right", padx=5, pady=10)


            # Umbenennen-Button
            edit_btn = tk.Button(ort_frame, text="✏️", font=("Arial", 14),
                                width=5, height=2,
                                command=lambda o=ort, i=idx: self.umbenennen(o, i))
            edit_btn.pack(side="right", padx=5, pady=10)




    def umbenennen(self, ort, idx):
        ort_frame = self.routes_button_frame.winfo_children()[idx]

        # Entferne alle vorhandenen Widgets im Frame
        for widget in ort_frame.winfo_children():
            widget.destroy()

        entry = tk.Entry(ort_frame, font=("Arial", 18))
        entry.insert(0, ort["name"])
        entry.pack(side="left", fill="x", expand=True, padx=10, pady=20)

        entry.bind("<FocusIn>", lambda e: subprocess.Popen(["matchbox-keyboard"]))

        def speichern():
            ort["name"] = entry.get()
            self.refresh()

        save_btn = tk.Button(ort_frame, text="✅", font=("Arial", 16),
                            command=speichern, width=3, height=1)
        save_btn.pack(side="right", padx=5, pady=10)


    def loesche_ort(self, index):
        del self.besondere_orte[index]
        self.refresh()
