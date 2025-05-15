import tkinter as tk
from View.Components.buttons import create_buttons, toggle_buttons

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)


        #Aufteilung
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


        #Buttons Rechts
        button_frame = tk.Frame(self, bg="lightgray")
        button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        for i in range(4):
            button_frame.rowconfigure(i, weight=1)
        button_frame.columnconfigure(0, weight=1)


        # Buttons erstellen
        buttons = create_buttons(button_frame)

        for i, btn in enumerate(buttons[:-1]):
            btn.grid(row=i, column=0, sticky="nsew", padx=10, pady=5)


        # Start/Stop-Button
        start_stop_button = buttons[-1]
        start_stop_button.config(text="Start", bg="green", command=lambda: toggle_buttons(start_stop_button))
        start_stop_button.grid(row=len(buttons) - 1, column=0, sticky="nsew", padx=10, pady=5)


        # Quit-Button
        quit_button = tk.Button(self, text="Quit", width=10, height=2, bg="red", fg="white", command=controller.destroy)
        quit_button.place(x=10, y=10)