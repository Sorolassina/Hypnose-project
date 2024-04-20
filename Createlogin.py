#import tkinter as tk
from tkinter import * 
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tkinter import messagebox, simpledialog
from tkinter import ttk
import pymongo 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from Config import *
class CreateLog ():
    def __init__(self, master=None,user_info=None):
        self.master=master
        self.user_info = user_info
        self.root = Toplevel(self.master)
        self.root.title(str(para_generaux['app_name']) + " " + "version"+str(para_generaux['version']))
        #self.root.title("Hypnose Manage DataBase")
        #self.root.iconbitmap('logo2.ico')

        self.root.iconbitmap(str(images['icone_application'])) 

        self.root.configure(bg="white")
        self.window_width = 1200
        self.window_height = 580
        self.center_window()
        myFontTitle = tkFont.Font(family="Poor Richard", size=20,weight="bold")
        myFontLabel = tkFont.Font(family="Times New Roman", size=10)
        myFontBouton = tkFont.Font(family="Arial", size=10)        
        self.root.resizable(False, False)
        self.load_background_image()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        # Création d'un style pour les widgets de thème
        style = ttk.Style()
        # Configuration du style pour arrondir les bordures du Frame
        style.configure('RoundedFrame.TFrame', borderwidth=5, relief='sunken', padding=(10,10))
        style.map('RoundedFrame.TFrame', background=[('selected', '#347083')])

        #Champ du formulaire d'inscription       
        zone1=ttk.Frame(self.root,style='RoundedFrame.TFrame')
        self.zone1=zone1
        self.zone1.place(x=250,y=100,width=700,height=250)
        titreZone=Label(self.zone1,text="Utilisateur",bg="#8c1959",font=myFontTitle,fg="white",justify="center",anchor="n")
        titreZone.place(relx=0.5, rely=0.02, anchor="n")
      
       # Nom 
        username_label = Label(self.zone1, text="Nom",bg="#8c1959", font=myFontLabel,fg="white")
        username_label.place(x=15, y=50)
        self.username_entry = Entry(self.zone1, width=30)
        self.username_entry.insert(0,self.user_info.get("Nom", ""))
        self.username_entry.place(x=100, y=50)
        # Liaison de la fonction à l'événement de perte de focus
        self.username_entry.bind("<KeyRelease>", lambda event: self.on_text_change(event, self.username_entry))

        # Email
        email_label = Label(self.zone1, text="Email", font=myFontLabel,bg="#8c1959", fg="white").place(x=15, y=80)
        self.email_entry = Entry(self.zone1, width=30)
        self.email_entry.insert(0,self.user_info.get("Email", ""))
        self.email_entry.place(x=100, y=80)
        self.email_entry.bind("<KeyRelease>", lambda event: self.on_text_change(event, self.email_entry))

        #Prenoms
        lastname_label = Label(self.zone1, text="Prénoms", font=myFontLabel,bg="#8c1959", fg="white").place(x=300, y=50)
        self.lastname_entry = Entry(self.zone1, width=40)
        self.lastname_entry.insert(0,self.user_info.get("Prénoms", ""))
        self.lastname_entry.place(x=400, y=50)
        self.lastname_entry.bind("<KeyRelease>", lambda event: self.on_text_change(event, self.lastname_entry))

        #Question
        question_label = Label(self.zone1, text="Questions", font=myFontLabel,bg="#8c1959", fg="white").place(x=300, y=80)
        value=["Quel est le nom de votre chat ?","Quel est votre groupe sanguin ?"]
        self.question_entry=ttk.Combobox(self.zone1,width=40,state="readonly",values=value)
        selected_index = value.index(self.user_info.get("Question", ""))
        self.question_entry.place(x=400, y=80)
        self.question_entry.current(selected_index)

        # Reponse
        reponse_label = Label(self.zone1, text="Réponse", font=myFontLabel,bg="#8c1959", fg="white").place(x=300, y=110)
        self.reponse_entry = Entry(self.zone1, width=40)
        self.reponse_entry.insert(0,self.user_info.get("Reponse", ""))
        self.reponse_entry.place(x=400, y=110)

        # Motdepasse
        password_label = Label(self.zone1, text="Mot de passe", font=myFontLabel,bg="#8c1959", fg="white").place(x=15, y=110)   
        self.password_entry = Entry(self.zone1, width=30)
        self.password_entry.insert(0,self.user_info.get("Mot de passe", ""))
        self.password_entry.place(x=100, y=110)
        # Limiter la longueur de l'entrée à 10 caractères       
        self.password_entry.bind("<FocusOut>", lambda event: self.validate_password(event, self.password_entry))
        
        # ConfirmMotdepasse
        Cfpassword_label = Label(self.zone1, text="Confirme MDP", font=myFontLabel,bg="#8c1959", fg="white").place(x=15, y=140)
        self.Cfpassword_entry = Entry(self.zone1, width=30)
        self.Cfpassword_entry.place(x=100, y=140)
        self.Cfpassword_entry.bind("<FocusOut>", lambda event: self.validate_password(event, self.Cfpassword_entry))

        # Précaution
        prec_label = Label(self.zone1,bg="#8c1959", 
                           text="*Votre mot de passe doit contenir au moins 10 caractères. \nDes caractères spéciaux, majuscules, minuscules et chiffres.",
                             font=myFontLabel, fg="white").place(x=300, y=140)
        
        # Boutons de création et abandon
        if self.user_info.get("Role","")=="Admin":
           Etat_button="normal"
        else:
           Etat_button="disabled"

        cancel_button = Button(self.zone1, width=10,bg="#39111C",fg="white",text="Cancel",font=myFontBouton, command=self.Cancellogin,cursor="hand2").place(x=555, y=200)
        update_button = Button(self.zone1, width=10,bg="#39111C",fg="white",text="Update",font=myFontBouton, command=self.UpdateUser,cursor="hand2").place(x=455, y=200)
        create_button = Button(self.zone1, width=10,bg="#39111C",fg="white",text="Create",font=myFontBouton, command=self.CreateUser,cursor="hand2",state=Etat_button).place(x=355, y=200)
    
        self.connnexion_local=str(database_local['host'])+str(database_local['port'])+'/'

    def on_text_change(self,event,textbox):
        # Récupérer le texte saisi dans le Entry
        input_text = textbox.get()    
        # Convertir en nom propre
        formatted_text = input_text.capitalize()   
        # Effacer le contenu actuel du Entry
        textbox.delete(0, END)
        # Insérer le texte formaté dans le Entry
        textbox.insert(0, formatted_text)
        
    def validate_password(self, event,textbox):
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
            messagebox.showerror("Erreur", "Le mot de passe doit être au moins de 10 caractères et contenir au moins 1 caractère spécial, 1 majuscule, 1 minuscule et 1 chiffre.",parent=self.root)
            textbox.delete(0,END)
            # Pour empêcher le focus de quitter le champ tant que la validation n'est pas réussie
            return False
        
    def UpdateUser(self):
        
        # Pour commençer, rassurons nous que toutes les zones de saisie sont renseignées
        if self.username_entry.get()=="" or self.email_entry.get()==""  or self.lastname_entry.get()=="" or self.question_entry.get()=="" or self.reponse_entry.get()=="" or self.password_entry.get()=="" or self.Cfpassword_entry.get()=="" :
            messagebox.showerror("Modification", "Merci de renseigner toutes les zones de saisie.",parent=self.zone1)
        # On se rassure également que la confirmation de mot de passe est conforme également
        elif self.password_entry.get()!= self.Cfpassword_entry.get():
            messagebox.showerror("Modification","Vos mots de passe ne sont pas conformes.",parent=self.root)
        else:

                try:
                    #client = pymongo.MongoClient("mongodb://localhost:27017/") # On ouvre la connexion à notre base Mongo
                    #db = client["Hypnose_base"] # On se connecte à notre base de données
                    #collection = db["Manage_Users"] # Ensuite on accède à la collection qui nous intéresse
                    
                    client = pymongo.MongoClient(self.connnexion_local) # "mongodb://localhost:27017/"
                    db = client[str(database_local['db_Users_name'])]
                    collection = db[str(database_local['db_users_table'])]
                                    
                    row_MDB = collection.find_one({"_id": self.user_info.get("_id", "")}) # On va vérifier ici que le mail qui a permis d'avoir accès à cette fenêtre existe
                    
                    if row_MDB != None :
                        # Critères de recherche pour trouver le document à mettre à jour
                        critere_recherche = {"_id": self.user_info.get("_id", "")}
                        # Opération de mise à jour à appliquer sur le document
                        #role1=self.user_info['Role']
                        if self.user_info['Role']=="Admin":
                            role="Admin"
                        else:
                            role="Autre"

                        operation_mise_a_jour = {"$set": {"Nom": self.username_entry.get(),
                                                          "Prénoms": self.lastname_entry.get(),
                                                          "Email": self.email_entry.get(),
                                                          "Question": self.question_entry.get(),
                                                          "Reponse": self.reponse_entry.get(),
                                                          "Mot de passe": self.password_entry.get(),
                                                          "Role": role 
                                                        
                                                          }
                                                          }
                        # Utilisation de find_one_and_update() pour trouver et mettre à jour le document
                        document_mis_a_jour = collection.find_one_and_update(
                                                                            critere_recherche,  # Critères de recherche
                                                                            operation_mise_a_jour # Opération de mise à jour
                                                                            )  

                        messagebox.showinfo("Modification","Vos informations ont été actualisées avec succès.",parent=self.root)

                        #messagebox.showinfo("Modification", f"Nouvelle donnée insérée avec l'ID: {}",parent=self.root)                    
                        # Définir les détails de l'e-mail
                        #sender_email = 'sorolassina58@gmail.com'
                        #sender_password ="mxcu kxhv jwym staa"

                        sender_email = para_smtp['sender_email']
                        sender_password =para_smtp['sender_password']

                        receiver_email = self.email_entry.get()
                        subject = 'Votre compte Hypnose a été mis à jour'
                        message = f"Bonjour {self.username_entry.get()} {self.lastname_entry.get()},\n\nVos informations à été modifiées avec succès. \
                                        \nSi vous êtes l'auteur de cette modification, considérez ce message à titre d'information uniquement.\
                                        \n\nNouveau mot de passe : {self.password_entry.get()}. \
                                        \n\nSi vous n'êtes pas certain que vous ou votre administrateur êtes l'auteur de cette modification, contactez votre administrateur immédiatement. \
                                        \n\nCordialement, \n\nL'équipe d'Hypnose."
                        
                        
                        
                        self.send_email(sender_email, sender_password, receiver_email, subject, message)
                        messagebox.showinfo("Modification", f"Un email a été envoyé à {receiver_email} suite à la modification de vos informations.",parent=self.root)
                        self.ReinitBox() # On réinitialise les textboxes  
                    else:
                        messagebox.showinfo("Modification", "Désolé mais nous ne parvenons pas à trouver cet utilisateur dans notre base.",parent=self.root) 

                    client.close()
                    self.root.destroy()
                    
                except Exception as ex:
                    messagebox.showerror("Connexion",f"Oups! L'erreur suivante nous empêche de nous connecter: {str(ex)}",parent=self.root)       
        

    def CreateUser(self):
                          
        # On vérifie que toutes les zones de saisies sont renseignées
        if self.username_entry.get()=="" or self.email_entry.get()=="" or self.lastname_entry.get()=="" or self.question_entry.get()=="" or self.reponse_entry.get()=="" or self.password_entry.get()=="" or self.Cfpassword_entry.get()=="" :
            messagebox.showerror("Création","Merci de renseigner toutes les zones de saisie.",parent=self.zone1)
        # On vérifie le mot de passe saisi est conforme au mdp confirmation
        elif self.password_entry.get()!= self.Cfpassword_entry.get():
            messagebox.showerror("Création","Vos mots de passe ne sont pas conformes.",parent=self.root)
        else:
    
                try:
                    #client = pymongo.MongoClient("mongodb://localhost:27017/") # On crée la connexion au serveur de la BD
                    #db = client["Hypnose_base"] # On se connecte à notre BD
                    #collection = db["Manage_Users"] #On récupère notre collection dans laquelle se trouve nos données utilisateur
                    
                    client = pymongo.MongoClient(self.connnexion_local) # "mongodb://localhost:27017/"
                    db = client[str(database_local['db_Users_name'])]
                    collection = db[str(database_local['db_users_table'])]
                    
                    row_MDB = collection.find_one({"_id": self.user_info.get("Email", "")}) # On recherche d'abord l'email saisi
                    
                    if row_MDB == None : # Si l'email saisi n'existe pas
                        
                        #role1=self.user_info['Role']
                        if self.user_info['Role']=="Admin":
                            role="Admin"
                        else:
                            role="Autre"

                        # On rassemble l'ensemble des infos à insérer dans une liste
                        operation_mise_a_jour = {"Nom": self.username_entry.get(),
                                                "Prénoms": self.lastname_entry.get(),
                                                "Email": self.email_entry.get(),
                                                "Question": self.question_entry.get(),
                                                "Reponse": self.reponse_entry.get(),
                                                "Mot de passe": self.password_entry.get(), 
                                                "Role": role 
                                                        }

                        # Insertion de la nouvelle donnée dans la collection et on stocke le résultat dans une variable
                        resultat = collection.insert_one(operation_mise_a_jour)

                        # Vérification du succès de l'opération en contrôlant cette variable
                        if resultat.inserted_id:
                            messagebox.showinfo("Création", f"Bienvenue {operation_mise_a_jour['Nom'] + operation_mise_a_jour['Prénoms']}, dans monde d'hypnose.",parent=self.root)                    
                            # Définir les détails de l'e-mail
                            #sender_email = 'sorolassina58@gmail.com'
                            #sender_password ="mxcu kxhv jwym staa"

                            # Configurer le serveur SMTP pour Gmail
                            sender_email = para_smtp['sender_email']
                            sender_password = para_smtp['sender_password']  # Port SMTP pour Gmail

                            receiver_email = self.email_entry.get()
                            subject = 'Votre compte Hypnose a été créé.'
                            message = f"Bonjour {self.username_entry.get()} {self.lastname_entry.get()},\n\nVotre compte vient d'être créé avec succès. \
                                    Si vous êtes l'auteur de cette création, considérez ce message à titre d'information uniquement.\
                                    \n\nNouveau mot de passe : {self.password_entry.get()}. \
                                    \n\nSi vous n'êtes pas certain que vous ou votre administrateur êtes l'auteur de cette création, contactez votre administrateur immédiatement. \
                                    \n\nCordialement, \n\nL'équipe d'Hypnose."
                            self.send_email(sender_email, sender_password, receiver_email, subject, message)
                            messagebox.showinfo("Création", f"Un email a été envoyé à {receiver_email} avec votre clé magique créée.",parent=self.root)
                            self.ReinitBox() # On réinitialise les textboxes                       
                        else:
                            messagebox.showinfo("Création", "Oups! Désolé nous n'arrivons pas à vous créer dans la base de données.",parent=self.root)

                        client.close() # On ferme la connexion au serveur par prudence    
                        self.root.destroy() # On ferme le formulaire de création
                    else:
                        messagebox.showinfo("Création", "Oups! ce nom d'utilisateur existe déjà, Veuillez en choisir un autre.",parent=self.root)

                    #client.close() # On ferme la connexion au serveur par prudence
                    #self.root.destroy() # On ferme le formulaire de création                       
                except Exception as ex:
                    messagebox.showerror("Création",f"Oups! cette erreur nous empêche de vous connecter : {str(ex)}",parent=self.root)       
 
    def ReinitBox(self):
        self.username_entry.delete(0,END)
        self.lastname_entry.delete(0,END)
        self.email_entry.delete(0,END)
        self.password_entry.delete(0,END)
        self.Cfpassword_entry.delete(0,END)
        self.question_entry.delete(0,END)
        self.reponse_entry.delete(0,END)
               
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def load_background_image(self):       
        background_image_pil = Image.open(images['background_createlogin'])
        resized_image = background_image_pil.resize((1200, 590), Image.LANCZOS)
        self.background_image_tk = ImageTk.PhotoImage(resized_image)
        self.background_label = ttk.Label(self.root, image=self.background_image_tk)
        self.background_label.place(x=0,y=0,relwidth=1, relheight=1)

    def Cancellogin(self):              
        self.root.destroy()

    def send_email(self,sender_email, sender_password, receiver_email, subject, message):
        # Configurer le serveur SMTP pour Gmail
        #smtp_server = 'smtp.gmail.com'
        #smtp_port = 587  # Port SMTP pour Gmail
        
        # Configurer le serveur SMTP pour Gmail
        smtp_server = para_smtp['smtp_server']
        smtp_port = para_smtp['smtp_port']  # Port SMTP pour Gmail
        
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

if __name__ == "__main__":    
    app = CreateLog() # Capture le focus sur la fenêtre CreateLog
    app.root.mainloop()
