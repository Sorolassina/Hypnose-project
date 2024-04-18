import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.load_background_image()

        self.username_entry = ttk.Entry(self.root)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.login_button = ttk.Button(self.root, text="Login", command=self.login)

        self.username_entry.pack()
        self.password_entry.pack()
        self.login_button.pack()

    def load_background_image(self):
        background_image_pil = Image.open("./images/Hypnose.jpg")
        resized_image = background_image_pil.resize((1380, 780), Image.LANCZOS)
        self.background_image_tk = ImageTk.PhotoImage(resized_image)
        self.background_label = ttk.Label(self.root, image=self.background_image_tk)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def login(self):
        # Votre logique de connexion ici
        # Si la connexion réussit, détruisez cette fenêtre et ouvrez la fenêtre utilisateur
        self.root.destroy()
        user_window = UserWindow()

class UserWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("User Window")

        self.load_background_image()

        # Autres widgets de la fenêtre utilisateur...
        
        self.root.mainloop()

    def load_background_image(self):
        background_image_pil = Image.open("./images/gramm.jpg")
        resized_image = background_image_pil.resize((1380, 780), Image.LANCZOS)
        self.background_image_tk = ImageTk.PhotoImage(resized_image)
        self.background_label = ttk.Label(self.root, image=self.background_image_tk)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
