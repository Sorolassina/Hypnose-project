import tkinter as tk
from tkinter import simpledialog

class CustomDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Nom:").grid(row=0)
        tk.Label(master, text="Email:").grid(row=1)
        tk.Label(master, text="Age:").grid(row=2)

        self.nom_entry = tk.Entry(master)
        self.email_entry = tk.Entry(master)
        self.age_entry = tk.Entry(master)

        self.nom_entry.grid(row=0, column=1)
        self.email_entry.grid(row=1, column=1)
        self.age_entry.grid(row=2, column=1)

    def apply(self):
        self.result = {
            "Nom": self.nom_entry.get(),
            "Email": self.email_entry.get(),
            "Age": self.age_entry.get()
        }

def show_custom_dialog():
    root = tk.Tk()
    dialog = CustomDialog(root, title="Saisir des informations")
    print(dialog.result)

    root.mainloop()

show_custom_dialog()
