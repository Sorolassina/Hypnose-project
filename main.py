import tkinter as tk
from Loginconnect import Login


if __name__ == "__main__":  
    root = tk.Tk()
    app = Login(root)  # Passer le widget parent (root) comme argument
    root.mainloop()