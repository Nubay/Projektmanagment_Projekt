import tkinter as tk

class NotificationDialog(tk.Toplevel):
    def __init__(self, parent, message="Aktion abgeschlossen.", button_text="OK", button_color="#4CAF50"):
        super().__init__(parent)
        self.title("Hinweis")
        self.geometry("400x200")
        self.resizable(False, False)
        self.configure(bg="white")

        # Zentrieren
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

        # Nachricht
        label = tk.Label(self, text=message, font=("Arial", 16), bg="white", wraplength=350, justify="center")
        label.pack(pady=40)

        # OK-Button
        ok_button = tk.Button(
            self, text=button_text, font=("Arial", 14), bg=button_color, fg="white",
            width=15, height=2, command=self.destroy
        )
        ok_button.pack(pady=10)

        self.transient(parent)
        self.grab_set()

