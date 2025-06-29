import tkinter as tk
import subprocess
import json
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

        # Scroll-Canvas
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

        self.json_path = os.path.join("Model", "JSONBesondereOrte", "besondere_orte.json")

        self.refresh()



    def load_orte(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []



    def save_orte(self, orte):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(orte, f, ensure_ascii=False, indent=2)



    def refresh(self):
        for widget in self.routes_button_frame.winfo_children():
            widget.destroy()

        orte = self.load_orte()

        for idx, ort in enumerate(orte):
            ort_name = ort.get("name", f"Besonderer Ort {idx + 1}")

            ort_frame = tk.Frame(self.routes_button_frame, bg="#a0a0a0", bd=1, relief="solid")
            ort_frame.pack(fill="x", padx=10, pady=5)

            label = tk.Label(ort_frame, text=f"{ort_name}", anchor="w", font=("Arial", 20, "bold"), bg="#a0a0a0")
            label.pack(side="left", padx=10, pady=20, expand=True, fill="x")

            delete_btn = tk.Button(
                ort_frame, text="❌", font=("Arial", 20),
                width=6, height=2,
                command=lambda i=idx: self.loesche_ort(i)
            )
            delete_btn.pack(side="right", padx=5, pady=10)

            edit_btn = tk.Button(
                ort_frame, text="✏️", font=("Arial", 20),
                width=6, height=2,
                command=lambda i=idx: self.umbenennen(i)
            )
            edit_btn.pack(side="right", padx=5, pady=10)




    def umbenennen(self, idx):
        orte = self.load_orte()
        ort = orte[idx]

        ort_frame = self.routes_button_frame.winfo_children()[idx]
        for widget in ort_frame.winfo_children():
            widget.destroy()

        # Validation-Funktion für Entry
        def validate_length(new_text):
            return len(new_text) <= 70

        vcmd = (ort_frame.register(validate_length), '%P')

        entry = tk.Entry(ort_frame, font=("Arial", 18), bg="#a0a0a0", fg="white", insertbackground="white",
                        validate='key', validatecommand=vcmd)
        entry.insert(0, ort["name"])
        entry.pack(side="left", fill="x", expand=True, padx=10, pady=20)

        def speichern():
            ort["name"] = entry.get()
            self.save_orte(orte)
            self.refresh()

        save_btn = tk.Button(ort_frame, text="✅", font=("Arial", 14),
                            command=speichern, width=5, height=2)
        save_btn.pack(side="right", padx=5, pady=10)







    def loesche_ort(self, idx):
        orte = self.load_orte()
        del orte[idx]
        self.save_orte(orte)
        self.refresh()
