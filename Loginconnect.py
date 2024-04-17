from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tkinter import messagebox, simpledialog
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymongo
from Createlogin import CreateLog
from UserformPrincipal import UserF
from tkinter import ttk
from tkinter.font import Font

class Login ():
   
    def __init__(self):
        self.root = Tk()
        self.root.title("HYPNOSE DataBase Manager")
        self.root.iconbitmap('logo2.ico')
        self.root.configure(bg="white")  
        self.window_width = 1380
        self.window_height = 780
        self.center_window(self.window_width,self.window_height)
        myFontTitle = tkFont.Font(family="Poor Richard", size=20,weight="bold")
        myFontLabel = tkFont.Font(family="Times New Roman", size=18)
        myFontBouton = tkFont.Font(family="Arial", size=13)
        self.load_background_image()
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        

        texte="“Welcome, valiant hero, to a world of adventure and challenge! May your courage and determination light your way, and may your actions forge the legend that awaits you.”"
        Title_label = Label(self.root, text=texte,justify="center", bg="#180633",font=("Arial",13), fg="white",anchor="n")
        Title_label.place(relx=0.5, rely=0, anchor="n")
        # Création d'un style
        stylezone = ttk.Style()
        # Configuration du style pour les frames avec des bords arrondis
        stylezone.configure('RoundedFrame.TFrame',background="#8c1959", borderwidth=50, relief='raised', padding=(10,10), borderradius=50)

        #Champ du formulaire d'inscription
        zone1=ttk.Frame(self.root,style='RoundedFrame.TFrame')       
        zone1.place(x=((self.window_width-700)//2),y=((self.window_height-300)//2),width=700,height=300)
        titreZone=Label(zone1,text="Hypnose connexion",font=myFontTitle,bg="#8c1959",fg="white",justify="center",anchor="n")
        titreZone.place(relx=0.5, rely=0.01, anchor="n")

        username_label = Label(zone1, text="Utilisateur", bg="#8c1959", font=myFontLabel, fg="white")
        username_label.place(x=40, y=90)
        self.username_entry = Entry(zone1, width=20,font=Font(size=14))
        self.username_entry.place(x=220, y=90)
        self.username_entry.bind("<KeyRelease>", lambda event: self.on_text_change(event, self.username_entry))

        password_label = Label(zone1, text="Mot de passe ", bg="#8c1959", font=myFontLabel, fg="white")
        password_label.place(x=40, y=130)
        self.password_entry = Entry(zone1,show="*", width=20,font=Font(size=14))
        self.password_entry.place(x=220, y=130)
        # Limiter la longueur de l'entrée à 10 caractères
        self.password_entry.bind("<FocusOut>", self.validate_password)
        
        self.login_button = Button(zone1, text="Valider",font=myFontBouton, bg="#39111C",fg="white",command=self.validate_login, width=10,cursor="hand2",activebackground="white", activeforeground="black")              
        self.login_button.place(width=190,x=500,y=70)
        self.forgot_password_button = Button(zone1, text="Mot de passe oublié ?",font=myFontBouton,bg="#39111C",fg="white", command=self.forgot_password,cursor="hand2",activebackground="white", activeforeground="black")
        self.forgot_password_button.place(width=190,x=500,y=105)
        delete_button = Button(zone1, width=10,bg="#39111C",fg="white",text="Supprimer utilisateur",font=myFontBouton, command=self.Delete_user,cursor="hand2",activebackground="white", activeforeground="black")
        delete_button.place(width=190,x=500,y=140)
        create_button = Button(zone1, width=10,bg="#39111C",fg="white",text="Créer utilisateur",font=myFontBouton, command=self.CreateUser,cursor="hand2",activebackground="white", activeforeground="black")
        create_button.place(width=190,x=500,y=175)

        # Création d'une police avec le style italique
        font_italic = tkFont.Font(family="Arial", size=13, slant="italic",underline=True)
        mod_userinfo_button = Button(zone1, text="Modifier vos informations ici !",fg="white",bg="#8c1959", borderwidth=0,font=font_italic, command=self.modification_InfoUser,cursor="hand2")
        mod_userinfo_button.place(x=210, y=180)  
         
    def on_text_change(self,event,textbox):
        # Récupérer le texte saisi dans le Entry
        input_text = textbox.get()    
        # Convertir en nom propre
        formatted_text = input_text.lower()   
        # Effacer le contenu actuel du Entry
        textbox.delete(0, END)
        # Insérer le texte formaté dans le Entry
        textbox.insert(0, formatted_text)
    
    def validate_password(self, event):
        new_text = event.widget.get()
             
        # Vérification de la présence de caractères spéciaux, de majuscules, de minuscules et de chiffres
        has_special = any(char for char in new_text if char in "!@#$%^&*()-_=+[{]}|;:',<.>/?")
        has_upper = any(char for char in new_text if char.isupper())
        has_lower = any(char for char in new_text if char.islower())
        has_digit = any(char for char in new_text if char.isdigit())
        
        if has_special and has_upper and has_lower and has_digit and len(new_text) >= 10:
            # Si tous les critères de validation sont satisfaits, la validation réussit
            return True
        else:
            # Sinon, afficher un message d'erreur ou prendre toute autre action nécessaire
            messagebox.showerror("Erreur", "Le mot de passe doit être au moins de 10 caractères et contenir au moins 1 caractère spécial, 1 majuscule, 1 minuscule et 1 chiffre.")
            self.password_entry.delete(0,END)
            # Pour empêcher le focus de quitter le champ tant que la validation n'est pas réussie
            return False
 
    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username=="" or password=="":
            messagebox.showerror("Connexion", "Nous avons besoin que vous renseignez toutes les zones de saisie.",parent=self.root)      
        else :
            
            try:
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client["Hypnose_manager"]
                if db is not None:
                    collection = db["Manage_Users"]
                    result = collection.find_one({"Email": username,"Mot de passe": password})
                    
                    if result is not None:
                        messagebox.showinfo("Connexion", f"“Bienvenue, {result['Nom']} {result['Prénoms']}.”",parent=self.root)
                        app = UserF()
                        #app.window.mainloop()
                        self.root.destroy()
                        
                    else:
                        messagebox.showerror("Connexion", "“Avez-vous oublié votre nom utilisateur et/ou mot de passe ?”",parent=self.root)
                        self.username_entry.focus_set()
                        self.username_entry.delete(0,END)
                        self.password_entry.delete(0,END)

            except Exception as ex:
                messagebox.showerror("Connexion",f"Oups! Nous avons rencontré pour nous connecter : {str(ex)}",parent=self.root)       
                           
    def forgot_password(self):
        email = simpledialog.askstring("Connexion", "Veuillez entrer votre nom utilisateur :",parent=self.root)
        if email is not None:
            try:
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client["Hypnose_manager"]
                collection = db["Manage_Users"]
                row_MDB = collection.find_one({"Email": email})
            
                if row_MDB != None:                    
                    reponse = simpledialog.askstring("Question", f"{row_MDB["Question"]}:",parent=self.root)

                    if reponse is not None: 

                        if reponse==row_MDB["Reponse"]:
                            new_password = simpledialog.askstring("Connexion", "Veuillez saisir votre nouveau mot de passe:",parent=self.root)  
                            # Critères de recherche pour trouver le document à mettre à jour
                            critere_recherche = {"_id": row_MDB["_id"]}
                            # Opération de mise à jour à appliquer sur le document
                            operation_mise_a_jour = {"$set": {"Mot de passe": new_password}}
                            # Utilisation de find_one_and_update() pour trouver et mettre à jour le document
                            document_mis_a_jour = collection.find_one_and_update(
                                                                                critere_recherche,  # Critères de recherche
                                                                                operation_mise_a_jour # Opération de mise à jour 
                                                                                )                 
                            # Définir les détails de l'e-mail
                            sender_email = 'sorolassina58@gmail.com'
                            sender_password ="mxcu kxhv jwym staa"
                            receiver_email = email
                            subject = 'Votre mot de passe Hypnose a été réinitialisé'
                            message = f"Bonjour {row_MDB["Nom"]} {row_MDB["Prénoms"]},\n\nVotre mot de passe a été récemment réinitialisé. \
                                            \nSi vous êtes l'auteur de cette réinitialisation, considérez ce message à titre d'information uniquement.\
                                            \n\nSi vous n'êtes pas certain que vous ou votre administratrice êtes l'auteur de cette réinitialisation, contactez votre administratrice immédiatement. \
                                            \n\nCordialement, \n\n\nL'équipe d'Hypnose."
                            self.send_email(sender_email, sender_password, receiver_email, subject, message)
                            messagebox.showinfo("MaJ", f"Un email a été envoyé à {email}.",parent=self.root)
    
                        elif reponse!=row_MDB["Reponse"]:
                            messagebox.showerror("Mot de passe oublié", "Réponse incorrecte. \nVeuillez contacter l'Administratrice.",parent=self.root) 
                         
                else:
                    messagebox.showerror("Mot de passe oublié", "Nous ne parvenons pas à trouver cet utilisateur. \nSi le problème persiste, veuillez contacter l'Administratrice.",parent=self.root) 
                
            except Exception as ex:
                messagebox.showerror("Connexion",f"Oups! Nous rencontrons un problème pour nous connecter: {str(ex)}",parent=self.root)       
            
            #On ferme la connexion
            client.close()

    def modification_InfoUser(self):

        email = simpledialog.askstring("Modification", "Veuillez saisir votre nom utilisateur:",parent=self.root)
        if email is not None:  
            try:
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client["Hypnose_manager"]
                collection = db["Manage_Users"]
                row_MDB = collection.find_one({"Email": email})

                if row_MDB != None: 
                    reponse = simpledialog.askstring("Question", f"{row_MDB["Question"]}:",parent=self.root)
                    if email is not None: 

                        if reponse ==row_MDB["Reponse"] : 
                            reponse = simpledialog.askstring("Modification", "Veuillez saisir votre mot de passe:",parent=self.root)
                            if reponse ==row_MDB["Mot de passe"] : 
                                user_info = row_MDB  # Remplacez ceci par les informations de l'utilisateur                      
                                app = CreateLog(self.root,user_info) 
                            else:
                                messagebox.showerror("Modification", "Oups! Mauvais mot de passe.",parent=self.root)
                        else:
                            messagebox.showerror("Modification", "Oups! Mauvaise réponse.",parent=self.root) 
                
                else:
                    messagebox.showerror("Connexion", "Désolez nous ne parvenons pas à retrouver cet utilisateur.",parent=self.root)
                    self.ReinitBox()

                client.close

            except Exception as ex:
                messagebox.showerror("Connexion",f"Oups! Nous rencontrons un problème pour nous connecter : {str(ex)}",parent=self.root)       
            
    def ReinitBox(self):
            self.username_entry.delete(0,END)
            self.password_entry.delete(0,END)
        
    def send_email(self,sender_email, sender_password, receiver_email, subject, message):
        # Configurer le serveur SMTP pour Gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Port SMTP pour Gmail

        # Créer un objet MIMEMultipart
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Ajouter le corps du message
        msg.attach(MIMEText(message, 'plain'))
        # Établir une connexion avec le serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Activer le mode TLS (Transport Layer Security)
        # Authentification avec le compte Gmail
        server.login(sender_email, sender_password)
        # Envoyer l'e-mail
        server.sendmail(sender_email, receiver_email, msg.as_string())
        # Fermer la connexion avec le serveur SMTP
        server.quit()

    def Delete_user(self):
                        
        email = simpledialog.askstring("Suppression", "Veuillez saisir votre nom utilisateur:",parent=self.root)

        if email is not None: 

            try:
                # Se connecter à la base de données MongoDB
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client["Hypnose_manager"]
                collection = db["Manage_Users"]
                
                # On recherche l'adresse dans la base
                row_MDB = collection.find_one({"Email": email})
                               
                if row_MDB != None : # Si l'email saisi existe
                    cle = simpledialog.askstring("Suppression", "Veuillez saisir votre mot de passe :",parent=self.root)
                    if cle==row_MDB["Mot de passe"] and row_MDB["Role"]=="Admin": # Si la clé est conforme à celle de l'administratrice et le mot de passe également
                        
                        email = simpledialog.askstring("Suppression", "Veuillez saisir le nom utilisateur à supprimer :",parent=self.root)
                        if email!=None:
                            # On recherche l'adresse dans la base
                            row_MDB = collection.find_one({"Email": email})
                            if row_MDB != None : # Si l'email saisi existe

                                if messagebox.askokcancel("Suppression", "Voulez-vous vraiment supprimer cet utilisateur ?",parent=self.root):
                                    # On rassemble l'ensemble des infos à insérer dans une liste
                                    Supp_user = row_MDB["_id"]
                                    # Supprimer l'utilisateur avec l'ID spécifié
                                    row_MDB = collection.delete_one({"_id": Supp_user})
                        
                                    messagebox.showinfo("Suppression", "L'utilisateur a été supprimé de la base hypnose.",parent=self.root)
                    else :
                        messagebox.showinfo("Suppression", "Seulement l'Administratrice peut supprimer un utilisateur.",parent=self.root)
            
            except Exception as e:
                messagebox.showinfo("Suppression", f"Oups! nous rencontrons une erreur pour supprimer l'utilisateur :{str(e)}",parent=self.root)

            finally:
                # Fermer la connexion à la base de données
                client.close()
        
    def CreateUser(self):
        
        email = simpledialog.askstring("Suppression", "Veuillez saisir votre nom utilisateur:",parent=self.root)

        if email is not None:
            
            try: 
                # Se connecter à la base de données MongoDB
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client["Hypnose_manager"]
                collection = db["Manage_Users"]
                
                # On recherche l'adresse dans la base
                row_MDB = collection.find_one({"Email": email})

                if row_MDB != None : # Si l'email saisi existe
                    cle = simpledialog.askstring("Création utilisateur", "Veuillez saisir votre mot de passe:",parent=self.root)
                    if cle==row_MDB["Mot de passe"] and row_MDB["Role"]=="Admin": # Si la clé est conforme à celle de l'administratrice et le mot de passe également
                        user_info =row_MDB   # Remplacez ceci par les informations de l'utilisateur                      
                        app = CreateLog(self.root,user_info) 
                    else :
                        messagebox.showinfo("Création", "Seulement l'Administratrice peut créer un utilisateur.",parent=self.root)
            
            except Exception as ex:
                            messagebox.showerror("Création",f"Oups! Nous rencontrons un problème pour vous connecter : {str(ex)}",parent=self.root)       

    def center_window(self,window_width,window_height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def load_background_image(self):       
        background_image_pil = Image.open("./images/gramm1.png")
        # Redimensionner l'image pour qu'elle corresponde à la taille de la fenêtre
        resized_image = background_image_pil.resize((1380, 780), Image.LANCZOS)
        self.background_image_tk = ImageTk.PhotoImage(resized_image)
        self.background_label = Label(self.root, image=self.background_image_tk)
        self.background_label.place(x=0,y=0,relwidth=1, relheight=1)
                   
    def on_closing(self):
        if messagebox.askyesno("Hypnose Data Manager", "Quittez l'application ?",parent=self.root):
           self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Login()
    app.run()