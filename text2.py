import tkinter as tk

class FormPopup:
    def __init__(self, parent):
        self.popup = tk.Toplevel(parent)
        self.popup.title("Formulaire")
        
        # Ajoutez ici les widgets de votre formulaire
        
        # Bloquer le focus sur la fenêtre popup
        self.popup.grab_set()

    def close(self):
        self.popup.destroy()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application principale")
        
        self.button_open_form = tk.Button(self.root, text="Ouvrir formulaire", command=self.open_form)
        self.button_open_form.pack(pady=10)

    def open_form(self):
        form = FormPopup(self.root)
        self.root.wait_window(form.popup)

root = tk.Tk()
app = MainApp(root)
root.mainloop()
