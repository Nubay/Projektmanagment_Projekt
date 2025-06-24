# View/Components/confirmation.py
import tkinter as tk
from tkinter import messagebox

def show_confirmation(message, on_confirm=None, title="Bestätigung", is_info=False):

    root = tk.Toplevel()
    root.title(title)
    root.geometry("400x220")
    root.resizable(False, False)
    root.grab_set()  # macht das Fenster modal

    w, h = 400, 260
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    # Nachricht
    label = tk.Label(
        root, text=message, wraplength=w - 40,
        justify="center", font=("Helvetica", 18)
    )
    label.pack(pady=(30, 40))

    # Buttons
    if is_info or on_confirm is None:
        ok_button = tk.Button(
            root, text="OK", width=12, height=2,
            command=root.destroy, font=("Helvetica", 16)
        )
        ok_button.pack(pady=10)
    else:
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        confirm_button = tk.Button(
            button_frame, text="Ja", width=12, height=2,
            command=lambda: [root.destroy(), on_confirm()],
            font=("Helvetica", 16)
        )
        confirm_button.grid(row=0, column=0, padx=10)

        cancel_button = tk.Button(
            button_frame, text="Nein", width=12, height=2,
            command=root.destroy, font=("Helvetica", 16)
        )
        cancel_button.grid(row=0, column=1, padx=10)


