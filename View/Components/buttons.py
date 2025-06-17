import tkinter as tk


def toggle_buttons(button):
    if button.config('text')[-1] == 'Start':
        button.config(text='Stop', bg='orange')
    else:
        button.config(text='Start', bg='green')
        
        

def create_buttons(parent):
    buttons = []
    btn_texts = ["Einstellung", "Routen" , "Standorte", "Exportieren", "Start"]
    colors = ["gray", "gray", "gray", "gray", "green"]

    for text, color in zip(btn_texts, colors):
        btn = tk.Button(parent, text=text, bg=color, fg="white", font=("Arial", 16))
        buttons.append(btn)
    
    return buttons
