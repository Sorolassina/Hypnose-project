import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Exemple de décochage d'une case à cocher")

# Création de la variable de contrôle de la case à cocher
checkbox_var = tk.IntVar()

# Création de la case à cocher
checkbox = ttk.Checkbutton(root, text="Coché", variable=checkbox_var)
checkbox.pack(pady=10)

def toggle_checkbox():
    if checkbox_var.get() == 1:  # Si la case à cocher est cochée
        checkbox_var.set(0)  # Décocher la case à cocher en mettant la valeur de la variable de contrôle à 0

# Création d'un bouton pour décocher la case à cocher
toggle_button = tk.Button(root, text="Décocher", command=toggle_checkbox)
toggle_button.pack(pady=5)

root.mainloop()
