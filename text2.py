import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview avec Barres de Défilement")

        # Création du Treeview
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("col1", "col2")
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Nom")
        self.tree.heading("col2", text="Âge")
        
        # Insertion de quelques éléments pour démonstration
        for i in range(1, 11):
            self.tree.insert("", "end", text=str(i), values=("Nom " + str(i), str(20 + i)))

        # Création de la barre de défilement verticale
        self.scrollbar_y = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        # Création de la barre de défilement horizontale
        self.scrollbar_x = tk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)

        # Placement du Treeview et des barres de défilement dans la grille
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Configuration des poids de la grille pour le redimensionnement
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
