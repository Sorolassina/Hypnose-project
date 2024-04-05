from doctest import *
import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import tkinter.font as tkFont

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Connexion à Hypnose")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        self.window_width = 400
        self.window_height = 200
        self.center_window()
        self.load_background_image()
        self.create_widgets()
        

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def load_background_image(self):
        myFontLabel = tkFont.Font(family="Times New Roman", size=10, weight="bold", slant="italic")
        background_image_pil = Image.open("./images/user.png")
        self.background_image_tk = ImageTk.PhotoImage(background_image_pil)
        self.background_label = Label(self.root, image=self.background_image_tk)
        self.background_label.place(relwidth=1, relheight=1)

    def create_widgets(self):
        myFontLabel = tkFont.Font(family="Times New Roman", size=10, weight="bold", slant="italic")
        username_label = Label(self.root, text="Nom d'utilisateur ", bg="black", font=myFontLabel, fg="white")
        username_label.place(x=15, y=50)
        self.username_entry = Entry(self.root, width=40)
        self.username_entry.place(x=125, y=50)

        password_label = tk.Label(self.root, text="Mot de passe ", bg="black", font=myFontLabel, fg="white")
        password_label.place(x=15, y=80)
        self.password_entry = Entry(self.root, width=40)
        self.password_entry.place(x=125, y=80)

        login_button = tk.Button(self.root, text="Connexion", command=self.validate_login, width=10)
        login_button.place(x=290, y=115)
        forgot_password_button = Button(self.root, text="Mot de passe oublié ?", command=self.forgot_password)
        forgot_password_button.place(x=150, y=115)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "utilisateur" and password == "motdepasse":
            messagebox.showinfo("Connexion réussie", "Connexion réussie en tant que {}".format(username))
            # Effacer les champs de texte
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)  
            # Ouvrir le formulaire principal

            self.root.quit()  # Arrête le boucle principale de l'application
            self.root.destroy()          
                       
        else:
            messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect")

    def forgot_password(self):
        email = simpledialog.askstring("Mot de passe oublié", "Veuillez saisir votre adresse e-mail:")
        if email == "utilisateur@example.com":
            new_password = simpledialog.askstring("Nouveau mot de passe", "Veuillez saisir votre nouveau mot de passe:")
            messagebox.showinfo("Mot de passe mis à jour", "Votre mot de passe a été mis à jour avec succès.")
            messagebox.showinfo("Email envoyé", "Un email a été envoyé à {} pour confirmer la modification de votre mot de passe.".format(email))
        else:
            messagebox.showerror("Erreur", "Adresse e-mail incorrecte.")

root=tk.Tk()
obj=Login(root)
root.mainloop