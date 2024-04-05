import tkinter as tk
from userforms.login import ConnexionApp
#from controllers import *

if __name__ == "__main__":  
    root = tk.Tk()
    app = ConnexionApp(root)  # Passer le widget parent (root) comme argument
    root.mainloop()