import tkinter as tk
from tkinter import ttk

def toggle_checkbox():
    if checkbox_var.get() == 1:  # Si la case à cocher est cochée
        checkbox.selection_clear()
        #checkbox.       # Décocher la case à cocher

root = tk.Tk()
root.title("Exemple de décochage d'une case à cocher")

# Création de la variable de contrôle de la case à cocher
checkbox_var = tk.IntVar()

# Création de la case à cocher
checkbox = ttk.Checkbutton(root, text="Coché", variable=checkbox_var)
checkbox.pack(pady=10)

# Création d'un bouton pour décocher la case à cocher
toggle_button = tk.Button(root, text="Décocher", command=toggle_checkbox)
toggle_button.pack(pady=5)

root.mainloop()
