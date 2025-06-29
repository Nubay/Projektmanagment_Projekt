import tkinter as tk
from tkinter import ttk

class ConfirmationDialog(tk.Toplevel):
    def __init__(self, parent, message="Möchten Sie fortfahren?", on_confirm=None, on_cancel=None):
        super().__init__(parent)
        self.title("Bestätigung")
        self.geometry("400x200")  # Größeres Fenster
        self.resizable(False, False)
        self.configure(bg="white")

        # Zentriere das Fenster auf dem Bildschirm
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

        # Inhalt
        label = tk.Label(self, text=message, font=("Arial", 16), bg="white")
        label.pack(pady=30)

        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=10)

        # Bestätigen-Button
        confirm_button = tk.Button(
            button_frame, text="Bestätigen", font=("Arial", 14), bg="#4CAF50", fg="white",
            width=15, height=2,
            command=lambda: self._handle(on_confirm)
        )
        confirm_button.grid(row=0, column=0, padx=10)

        # Abbrechen-Button
        cancel_button = tk.Button(
            button_frame, text="Abbrechen", font=("Arial", 14), bg="#f44336", fg="white",
            width=15, height=2,
            command=lambda: self._handle(on_cancel)
        )
        cancel_button.grid(row=0, column=1, padx=10)

        self.transient(parent)
        self.grab_set()  # Macht das Fenster modal

    def _handle(self, callback):
        self.destroy()
        if callback:
            self.after(10, callback)


