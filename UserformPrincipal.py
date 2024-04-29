from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tkinter import messagebox, simpledialog
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter as tk
import pymongo
import datetime
from LoadFile import App
from datetime import datetime
from gridfs import GridFS
import tempfile
import subprocess
import platform
from bson import ObjectId
import time

class UserF():
    def __init__(self):
        self.window=tk.Tk()     
        self.window.title("Hypnose Data Manager")
        self.window.iconbitmap('logo2.ico')
        self.window.configure(bg="white")
        self.window_width = 1380
        self.window_height = 780
        self.center_window(self.window_width,self.window_height)
        myFontTitle = tkFont.Font(family="Times New Roman", size=20, weight="bold")
        myFontLabel = tkFont.Font(family="Times New Roman", size=12)
        myFontBouton = tkFont.Font(family="Arial", size=10)
        self.load_background_image()
        self.window.resizable(False, False)
        self.window.focus_force()
        
        # Création d'un style pour les widgets de thème
        self.style = ttk.Style()
        # Configuration du style pour arrondir les bordures du Frame
        self.style.configure('RoundedFrame.TFrame', borderwidth=1, relief='groove', padding=(10,10))
        self.style.map('RoundedFrame.TFrame', background=[('selected', '#FFFFFF')])       
        #Champ du formulaire d'inscription
        zone1=ttk.Frame(self.window,style='RoundedFrame.TFrame')       
        zone1.place(x=((self.window_width-1330)//2),y=((self.window_height-730)//2),width=1330,height=730)
  
        # Définition du style pour la couleur de fond du cadre
        self.style = ttk.Style()
        self.style.configure('My.TFrame', background='#FFFFFF')  # Couleur de fond grise
        # Création du cadre avec une bordure et une couleur de fond
        Cadre_affichage = ttk.Frame(zone1, borderwidth=2, style='My.TFrame',relief='groove')
        Cadre_affichage.place(x=100,y=55,width=1010,height=655)
         
         # Création du Treeview avec 7 colonnes
        self.tree = ttk.Treeview(Cadre_affichage, columns=("Date",'Titre','Auteur','Pages','Type','Langue','Id'))
        
        # Définition des en-têtes de colonnes de ma treeview
        self.tree.heading("Date", text="Date")
        self.tree.heading('Titre', text='Titre')
        self.tree.heading('Auteur', text='Auteur')      
        self.tree.heading("Pages", text="Pages")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Langue", text="Langue")
        self.tree.heading("Id", text="Id")
        
        self.tree["show"]="headings" # On affiche les entêtes

        # Définition de la largeur des colonnes
        self.tree.column("Date", width=70)
        self.tree.column('Titre', width=150)
        self.tree.column('Auteur', width=150)
        self.tree.column("Pages", width=50)
        self.tree.column("Type", width=150)
        self.tree.column("Langue", width=100)
        self.tree.column("Id", width=50)
        
        self.tree.pack(expand=True,fill='both')

        # Configuration des événement liés à ma treeview
        self.tree.bind("<ButtonRelease-1>", self.on_treeview_select)
        self.tree.bind("<Double-1>", self.display_pdf) # Afficher le document après un double clic dessus
        self.tree.bind("<Enter>", lambda event: self.tree.config(cursor="hand2")) # Donner la forme de main au curseur une fois vous êtes sur la treeview
        self.tree.bind("<Leave>", lambda event: self.tree.config(cursor="")) # Donner la forme normale au curseur une fois vous quittez la treeview

        # Création de la barre de défilement verticale
        self.scrollbar_y = tk.Scrollbar(Cadre_affichage, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        # Création de la barre de défilement horizontale
        self.scrollbar_x = tk.Scrollbar(Cadre_affichage, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)

        # Placement du Treeview et des barres de défilement dans la grille
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Configuration des poids de la grille pour le redimensionnement
        Cadre_affichage.grid_rowconfigure(0, weight=1)
        Cadre_affichage.grid_columnconfigure(0, weight=1)

        # Lier la fonction à l'événement <<TreeviewSelect>>
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)
        self.scrollbar_x.bind("<B1-Motion>", lambda event: self.tree.xview_moveto(event.x))
        self.scrollbar_y.bind("<B1-Motion>", lambda event: self.tree.yview_moveto(event.y))
        
        # Création du cadre à gauche
        Cadre_box = ttk.Frame(zone1, borderwidth=2, style='My.TFrame',relief='groove')
        Cadre_box.place(x=20,y=20,width=80,height=690)
 
        # Création du cadre pour les boutons
        Cadre_bouton = ttk.Frame(zone1, borderwidth=2, style='My.TFrame',relief="solid")
        Cadre_bouton.place(x=1120,y=20,width=190,height=690)

        self.stylcheckbox = ttk.Style() # On va configurer un style de checkbox qu'on appliquera à nos checkbox
        self.stylcheckbox.configure("White.TCheckbutton", background="white",borderwidth=0)

        # Configuration du bouton création
        quit_button = Button(Cadre_bouton, width=20,text="Quitter",bg="red",foreground="white",font=myFontBouton, command=lambda: self.window.destroy(),cursor="hand2").place(x=8, y=20)

        # Creation du checkbox base cloud
        self.basecloud_var = tk.IntVar()
        self.checkbox_basecloud = ttk.Checkbutton(Cadre_bouton, text="Stockage cloud",state="disabled", cursor="hand2",variable=self.basecloud_var,style="White.TCheckbutton", command=self.CheckBoxDB_manage)
        self.checkbox_basecloud.place(x=8,y=60)

        #Creation du checkbox base local
        self.baselocale_var = tk.IntVar(value=1)
        self.checkbox_baseclocale = ttk.Checkbutton(Cadre_bouton, text="Stockage local", cursor="hand2",variable=self.baselocale_var,style="White.TCheckbutton", command=self.CheckBoxDB_manage)
        self.checkbox_baseclocale.place(x=8,y=90)

        #On configure le checkbox doc attente
        self.docattente_var = tk.IntVar(value=1) # Variable censé recueillir l'état de notre chkbox
        self.checkbox_docattente = ttk.Checkbutton(Cadre_bouton, text="Documents en attente", cursor="hand2",variable=self.docattente_var,style="White.TCheckbutton", command=self.CheckBoxCollect_manage)
        self.checkbox_docattente.place(x=8,y=120)

        #On configure le checkbox docs validés
        self.docvalide_var = tk.IntVar() # Variable censé recueillir l'état de notre chkbox
        self.checkbox_docvalide = ttk.Checkbutton(Cadre_bouton, text="Documents certifiés",state="disabled", cursor="hand2",variable=self.docvalide_var,style="White.TCheckbutton", command=self.CheckBoxCollect_manage)
        self.checkbox_docvalide.place(x=8,y=150)

        # On va créer les variables globales
        self.cloudBD=tk.StringVar() #Stocker la connexion au cloud
        self.localBD=tk.StringVar() #Stocker la connexion au local
        self.certifie=tk.StringVar() #Stocker la connexion aux documents certifiés
        self.noncertifie=tk.StringVar() #Stocker la connexion aux documents non validés

        # Creation du button create 
        create_button = Button(zone1, width=15,text="Charger fichiers",font=myFontBouton, command=self.loading_file,cursor="hand2")
        create_button.place(x=970, y=20) 

        # On crée le button update   
        self.update_button = Button(Cadre_bouton, width=20,text="Transférer",font=myFontBouton, command=self.transfer_selected_documents,state="disabled",cursor="hand2")
        self.update_button.place(x=8, y=180) 

        # On crée le button delete
        delete_button = Button(Cadre_bouton, width=20,text="Supprimer",font=myFontBouton, command=self.remove_file,cursor="hand2")
        delete_button.place(x=8, y=270)

        # On crée la zone de saisie de recherche
        self.lookvalue_entry = ttk.Entry(zone1, background='#FFFFFF')
        self.lookvalue_entry.place(x=460, y=20,width=350,height=28) 

        self.lookvalue_entry.bind("<KeyRelease>", self.filter_tree) # Evénément à chaque clique sur une touche dans la zone de saisie de recherche

        # Un label pour compter le nombre d'éléments dans la treeview
        self.labelCount=Label(zone1,text='',font=myFontLabel)
        self.labelCount.place(x=150, y=20)

        # Création du bouton recherche
        Defilter_button = Button(zone1, width=15,text="Défiltrer",foreground="black",font=myFontBouton, command=self.deselect,cursor="hand2")      
        Defilter_button.place(x=825, y=20)

        # Creation du label
        look_label = Label(zone1, width=15,text="Rechercher ici :",foreground="black",font=myFontLabel)      
        look_label.place(x=300, y=20)    

        #Choix pour changement de Storage et de Base
        self.changestorage_var = tk.IntVar(value=0) # Stocker l'état de la chekboxe changement de DB
        self.checkbox_ChangeDB = ttk.Checkbutton(Cadre_bouton, text="Changer de Storage ?", cursor="hand2",variable=self.changestorage_var,style="White.TCheckbutton",state="disabled",command=self.changerbase)
        self.checkbox_ChangeDB.place(x=8, y=210)

        # Choix pour changer de collection
        self.changebase_var = tk.IntVar(value=0) # Stocker l'état de la chekboxe changement de collection
        self.checkbox_ChangeCollection = ttk.Checkbutton(Cadre_bouton, text="Changer de Base ?", cursor="hand2",variable=self.changebase_var,style="White.TCheckbutton",state="disabled",command=self.changercollection)
        self.checkbox_ChangeCollection.place(x=8, y=230)

        # Créer une barre de progression avec une hauteur plus petite
        style = ttk.Style()
        style.configure("Custom.TProgressbar", thickness=10,foreground='green', background='green')  # Épaisseur de la barre de progression
        style.layout("Custom.TProgressbar", [('Custom.Progressbar.trough', {'sticky': 'nswe', 'children': [('Custom.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})]})])

        # On va créer la barre de progression
        self.progress_bar = ttk.Progressbar(zone1, orient='horizontal', length=1010, mode='determinate',style="Custom.TProgressbar")
        self.progress_bar.place(x=100,y=710)
        

        #Création de nos variables
        self.EltAChanger={'Id':"",'Storage':"",'Base':""}
        self.Ancien_storage=None
        self.Ancienne_bases=None
        
        self.Client=None
        self.db=tk.StringVar()
        #Récupération des données depuis la Storage de données locale MongoDB 
        self.Appel_loading_data()

        #On va centre toutes les données de ma tree view pour un meilleur affichage
        for col in self.tree["columns"]: 
            self.tree.column(col, anchor="center")

        self.window.mainloop()

    def deselect(self):
        self.tree.selection_remove(self.tree.selection()) #On supprime tous les filtres de notre tableau
        self.lookvalue_entry.delete(0,END) # On efface le contenu de la zone de saisie recherche
        self.tree.update_idletasks() # On raffraichit notre treeview
     
    def changerbase(self):
        
        if self.changestorage_var.get() == 1 and self.EltAChanger['Id']!=None: # On vérifie  si la case changement de storage est oui et si un élément est sélectionné
            self.update_button.config(state="normal") # On rend disponible le boutton mise à jour
            
            if self.EltAChanger['Storage']=="Cloud": # Si le storage initial est Cloud
                self.Ancien_storage=self.EltAChanger['Storage'] # On sauvegarde dab la Storage d'origine dans une variable
                self.EltAChanger['Storage']= "Locale"  # Ensuite le nom de mon nouveau storage devient Locale
            elif self.EltAChanger['Storage']=="Locale": # Si le storage initial est Local
                self.Ancien_storage=self.EltAChanger['Storage'] # On sauvegarde dab la Storage d'origine dans la variable Ancien_storage
                self.EltAChanger['Storage']="Cloud" # L"ancien étant sauvegardé, on attribue la valeur Cloud à notre storage

        elif self.changestorage_var.get() == 0 and self.EltAChanger['Id']!=None:
            self.EltAChanger['Storage']=self.Ancien_storage

        if self.changestorage_var.get() == 0 and self.changebase_var.get() == 0: 
            
            self.update_button.config(state="disabled")

    def changercollection(self):
        
        if self.changebase_var.get() == 1 and self.EltAChanger['Id']!=None :
            self.update_button.config(state="normal")
            if self.EltAChanger['Base']=="Hypnose_documents_en_attente":
                self.Ancienne_bases=self.EltAChanger['Base']
                self.EltAChanger['Base']= "Hypnose_documents_validés" 
            elif self.EltAChanger['Base']=="Hypnose_documents_validés":
                self.Ancienne_bases=self.EltAChanger['Base']
                self.EltAChanger['Base']="Hypnose_documents_en_attente"

        elif self.changebase_var.get() == 0 and self.EltAChanger['Id']!=None:
            self.EltAChanger['Base']=self.Ancienne_bases

        if self.changestorage_var.get() == 0 and self.changebase_var.get() == 0:
            
            self.update_button.config(state="disabled")   

    def CheckBoxDB_manage(self):
    # Fonction de rappel pour exécuter lorsque la case à cocher est cochée ou décochée

        if self.basecloud_var.get() == 1 and self.baselocale_var.get() == 0 :           
            self.checkbox_baseclocale.config(state="disabled")
            self.Appel_loading_data()

        elif self.baselocale_var.get() == 1 and self.basecloud_var.get() == 0  :           
            self.checkbox_basecloud.config(state="disabled")
            self.Appel_loading_data()

        elif self.basecloud_var.get() == 0 and self.baselocale_var.get() == 0 :           
            self.checkbox_baseclocale.config(state="normal")
            self.checkbox_basecloud.config(state="normal")
            self.Appel_loading_data()

    def CheckBoxCollect_manage(self):
    # Fonction de rappel pour exécuter lorsque la case à cocher est cochée ou décochée
        if self.docvalide_var.get() == 1 and self.docattente_var.get() == 0 :           
            self.checkbox_docattente.config(state="disabled")
            self.Appel_loading_data()

        elif self.docattente_var.get() == 1 and self.docvalide_var.get() == 0  :           
            self.checkbox_docvalide.config(state="disabled")
            self.Appel_loading_data()
        
        elif self.docvalide_var.get() == 0 and self.docattente_var.get() == 0 :           
            self.checkbox_docattente.config(state="normal")
            self.checkbox_docvalide.config(state="normal")
           
            self.Appel_loading_data()

    def count_elt(self):
           # Compter le nombre d'éléments dans la TreeView
           num_elements = len(self.tree.get_children())
           # Mettre à jour l'étiquette avec le nombre d'éléments
           self.labelCount.config(text=f"{num_elements} documents listés /")
   
    def Appel_loading_data(self) :
        if self.basecloud_var.get() == 1 and self.docvalide_var.get() == 1:
           self.loading_data()
           self.count_elt()
           self.checkbox_ChangeCollection.config(text="Mettre en attente")
           self.checkbox_ChangeDB.config(text="Transférer en local")

        elif self.baselocale_var.get() == 1 and self.docvalide_var.get() == 1:
           self.loading_data()
           self.count_elt()
           self.checkbox_ChangeCollection.config(text="Mettre en attente")
           self.checkbox_ChangeDB.config(text="Transférer sur le cloud")

        elif self.baselocale_var.get() == 1 and self.docattente_var.get() == 1:
           self.loading_data()
           self.count_elt()
           self.checkbox_ChangeCollection.config(text="Valider le(s) documents")
           self.checkbox_ChangeDB.config(text="Transférer sur le cloud")

        elif self.basecloud_var.get() == 1 and self.docattente_var.get() == 1:
           self.loading_data()
           self.count_elt()
           self.checkbox_ChangeCollection.config(text="Valider le(s) documents")
           self.checkbox_ChangeDB.config(text="Transférer vers le local")
        else:
            # Exemple d'utilisation pour vider le Treeview
            self.clear_treeview()
            self.count_elt()
            
    def loading_file(self):
        app = App(self.window) 
    
    def filter_tree(self,event=None):
        filter_text =  self.lookvalue_entry.get().lower()
        for item in self.tree.get_children():
            item_values = self.tree.item(item, 'values')
            if any(filter_text in str(value).lower() for value in item_values):
                self.tree.selection_add(item)
            else:
                self.tree.selection_remove(item)

    # Définir une fonction pour gérer la sélection dans la Treeview
    def on_treeview_select(self,event):
        # Obtenez les ID des éléments sélectionnés
        selected_items = event.widget.selection()
        
        # Vérifiez s'il y a des éléments sélectionnés
        if selected_items:
            self.checkbox_ChangeDB.config(state="normal")
            self.checkbox_ChangeCollection.config(state="normal")
        else:
            self.checkbox_ChangeDB.config(state="disabled")
            self.checkbox_ChangeCollection.config(state="disabled")
 
    def load_files_from_gridfs(self,db):
              
        fs = GridFS(db)

        # Récupérer les fichiers depuis GridFS
        files = fs.find()
       
        for file in files:
            date_objet=file.uploadDate
            
            # Créer un tuple contenant les valeurs à afficher dans le Treeview
            metadata_values = (
                date_objet.date(),
                file.metadata.get('filename', ''),
                file.metadata.get('author', ''),# Récupérer l'auteur depuis les métadonnées
                file.metadata.get('pages', ''), # Récupérer le nombre de pages depuis les métadonnées
                file.metadata.get('type', ''),  # Récupérer le type depuis les métadonnées
                file.metadata.get('language', ''),  # Récupérer la langue depuis les métadonnées                
                file._id,

                  # Récupérer le contenu depuis les métadonnées
            )
            # Insérer les valeurs dans le Treeview
            self.tree.insert('', 'end', text=file._id, values=metadata_values)          

    def open_pdf_file(self,file_path):
        system = platform.system()
        if system == 'Windows':
            subprocess.Popen(['start', '', file_path], shell=True)
        elif system == 'Linux':
            subprocess.Popen(['xdg-open', file_path])
        elif system == 'Darwin':  # macOS
            subprocess.Popen(['open', file_path])
        else:
            pass
           

    def display_pdf(self, event):
        
        selected_item = self.tree.selection()
        if selected_item:
            # Récupérer l'ID de l'élément sélectionné
            item_id = self.tree.item(selected_item, 'text')

            # Créer un ObjectId à partir d'une chaîne hexadécimale
            object_id = ObjectId(item_id)

            # Connexion à MongoDB
            fs = GridFS(self.db)
            # Récupérer le fichier depuis GridFS en utilisant son ID
            file = fs.get(object_id)
            # Accéder au contenu du fichier
            file_content = file.read()

            # Créer un fichier temporaire pour stocker le contenu du PDF
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
                
            # Ouvrir le fichier temporaire avec le lecteur PDF par défaut sur l'ordinateur
            self.open_pdf_file(temp_file_path)

    def center_window(self,window_width,window_height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def load_background_image(self):       
        background_image_pil = Image.open("./images/Hypnose.jpg")
        resized_image = background_image_pil.resize((1380, 780), Image.LANCZOS)
        self.background_image_tk = ImageTk.PhotoImage(resized_image)
        self.background_label = ttk.Label(self.window, image=self.background_image_tk)
        self.background_label.place(x=0,y=0,relwidth=1, relheight=1)

    def loading_data(self):
        count_file=0
        # On actualise la barre de progression
        self.progress_bar['value'] = (count_file / 3) * 100                               
        self.progress_bar.update()

        try:
            if self.basecloud_var.get() == 1 :
                count_file=1
                # On actualise la barre de progression
                self.progress_bar['value'] = (count_file / 3) * 100                               
                self.progress_bar.update()

                # Connexion à la Storage de données
                #self.Client.close()
                self.Client = pymongo.MongoClient("mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/")
               
                self.EltAChanger['Storage']="Cloud" 

                if self.docattente_var.get() == 1 :
                    count_file=2
                    # On actualise la barre de progression
                    self.progress_bar['value'] = (count_file / 3) * 100                               
                    self.progress_bar.update()

                    #try:
                    self.db=self.Client["Hypnose_documents_en_attente"]
                    #except Exception as e:
                        #messagebox.showerror("Connexion", f"Erreur lors du chargement des données : {e}",parent=self.window)
    
                    self.load_files_from_gridfs(self.db)       
                    
                elif self.docvalide_var.get() == 1 :
                    count_file=2
                    # On actualise la barre de progression
                    self.progress_bar['value'] = (count_file / 3) * 100                               
                    self.progress_bar.update()

                    #Base = db["Hypnose_documents_validés"]
                    self.EltAChanger['Base']="Hypnose_documents_validés" #On récupère la Base sélectionnée
                     
                    # Exemple d'utilisation pour vider le Treeview
                    self.clear_treeview()
                    # Insertion des données dans le Treeview
                    self.db=self.Client["Hypnose_documents_validés"]
                    self.load_files_from_gridfs(self.db)                    
                    
                else:
                    messagebox.showerror("Affichage", "Aucune table n'a été sélectionnée.")
                      
                
            elif self.baselocale_var.get() == 1 :
                count_file=1
                # On actualise la barre de progression
                self.progress_bar['value'] = (count_file / 3) * 100                               
                self.progress_bar.update()

                # Connexion à la Storage de données
                #self.Client.close()
                self.Client = pymongo.MongoClient("mongodb://localhost:27017/")
                self.EltAChanger['Storage']="Locale" #On récupère la Storage sélectionnée

                if self.docattente_var.get() == 1 :
                    count_file=2
                    # On actualise la barre de progression
                    self.progress_bar['value'] = (count_file / 3) * 100                               
                    self.progress_bar.update()

                    #Base = db["Hypnose_documents_en_attente"]
                    self.EltAChanger['Base']="Hypnose_documents_en_attente" #On récupère la Base sélectionnée
                    # Exemple d'utilisation pour vider le Treeview
                    self.clear_treeview()
                    # Insertion des données dans le Treeview
                    self.db=self.Client["Hypnose_documents_en_attente"]
                    self.load_files_from_gridfs(self.db)             

                elif self.docvalide_var.get() == 1 :
                    count_file=2
                    # On actualise la barre de progression
                    self.progress_bar['value'] = (count_file / 3) * 100                               
                    self.progress_bar.update()

                    #Base = self.db["Hypnose_documents_validés"]
                    self.EltAChanger['Base']="Hypnose_documents_validés" #On récupère la Base sélectionnée
                    # Récupération de tous les documents dans la Base
                    #cursor = Base.find()
                    # Exemple d'utilisation pour vider le Treeview
                    self.clear_treeview()

                    self.db=self.Client["Hypnose_documents_validés"]
                    self.load_files_from_gridfs(self.db)
               
                else:
                    messagebox.showerror("Affichage", "Aucune table n'a été sélectionnée.")
                     
            else:
                messagebox.showerror("Affichage", "Aucune Storage n'a été sélectionnée.")
                 
        except Exception as e:
            messagebox.showerror("Connexion", f"Erreur lors du chargement des données : {e}",parent=self.window)

        # On actualise la barre de progression                              
        self.progress_bar.stop()
        #self.Client.close()
        
    def transfer_selected_documents(self):

        try:
            source_client=None
            destination_client=None
            source_collect=None
            destination_collect=None
            
            selected_items = self.tree.selection()
            if selected_items:

                # ON CHANGE DE LIEU DE STOCKAGE
                if  self.changestorage_var.get()==1: 

                    # ON CHANGE EGALEMENT DE BASE ET DE LIEU DE STOCKAGE
                    if  self.changebase_var.get()==1: # On configure la Base si elle a été changée     
                       
                        # DESTINATION CLOUD
                        if self.EltAChanger['Storage']=='Cloud': # On configure la Storage de données pour se connecter
                            source_client = pymongo.MongoClient('mongodb://localhost:27017/')
                            destination_client = pymongo.MongoClient('mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/') 
                            
                            if self.EltAChanger['Base']=='Hypnose_documents_en_attente':
                                source_collect = source_client[str(self.Ancienne_bases)]
                                destination_collect = destination_client['Hypnose_documents_en_attente']
                            elif self.EltAChanger['Base']=='Hypnose_documents_validés':
                                source_collect = source_client[str(self.Ancienne_bases)]
                                destination_collect = destination_client['Hypnose_documents_validés']
                        
                        # DESTINATION LOCALE
                        elif self.EltAChanger['Storage']=='Locale': # On configure la Storage de données pour se connecter
                            destination_client = pymongo.MongoClient('mongodb://localhost:27017/')
                            source_client = pymongo.MongoClient('mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/') 
                            
                            if self.EltAChanger['Base']=='Hypnose_documents_en_attente':
                                source_collect = source_client[str(self.Ancienne_bases)]
                                destination_collect = destination_client['Hypnose_documents_en_attente']
                            elif self.EltAChanger['Base']=='Hypnose_documents_validés':
                                source_collect = source_client[str(self.Ancienne_bases)]
                                destination_collect = destination_client['Hypnose_documents_validés']

                    
                    # ON CHANGE DE LIEU DE STOCKAGE ET ON NE CHANGE PAS DE BASE
                    elif  self.changebase_var.get()==0: # Supposons que la base de stockage ne change pas 

                        # DESTINATION CLOUD
                        if self.EltAChanger['Storage']=='Cloud': # On configure la Storage de données pour se connecter
                            source_client = pymongo.MongoClient('mongodb://localhost:27017/')
                            destination_client = pymongo.MongoClient('mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/') 

                            if self.EltAChanger['Base']=='Hypnose_documents_en_attente':
                                source_collect = source_client['Hypnose_documents_en_attente']
                                destination_collect = destination_client['Hypnose_documents_en_attente']
                            elif self.EltAChanger['Base']=='Hypnose_documents_validés':
                                source_collect = source_client['Hypnose_documents_validés']
                                destination_collect = destination_client['Hypnose_documents_validés']

                        # DESTINATION LOCALE
                        elif self.EltAChanger['Storage']=='Locale': # On configure la Storage de données pour se connecter                            
                            source_client = pymongo.MongoClient('mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/') 
                            destination_client = pymongo.MongoClient('mongodb://localhost:27017/')

                            if self.EltAChanger['Base']=='Hypnose_documents_en_attente':
                                source_collect = source_client['Hypnose_documents_en_attente']
                                destination_collect = destination_client['Hypnose_documents_en_attente']
                            elif self.EltAChanger['Base']=='Hypnose_documents_validés':
                                source_collect = source_client['Hypnose_documents_validés']
                                destination_collect = destination_client['Hypnose_documents_validés']

                # ON NE CHANGE PAS DE STORAGE
                elif  self.changestorage_var.get()==0: # Si le bouton changer de Storage a été coché

                    # ON NE CHANGE PAS DE STORAGE MAIS ON CHANGE DE BASE
                    if  self.changebase_var.get()==1: # On configure la Base si elle a été changée     
                       
                        # Si la destination est le cloud
                        if self.EltAChanger['Storage']=='Cloud': # On configure la Storage de données pour se connecter
                            source_client = pymongo.MongoClient('mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/')
                            destination_client = pymongo.MongoClient('mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/') 
                            
                            if self.EltAChanger['Base']=='Hypnose_documents_en_attente':
                                source_collect = source_client[str(self.Ancienne_bases)]
                                destination_collect = destination_client['Hypnose_documents_en_attente']
                            elif self.EltAChanger['Base']=='Hypnose_documents_validés':
                                source_collect = source_client[str(self.Ancienne_bases)]
                                destination_collect = destination_client['Hypnose_documents_validés']
                        
                        # Si la destinatination est le local
                        elif self.EltAChanger['Storage']=='Locale': # On configure la Storage de données pour se connecter
                            source_client = pymongo.MongoClient('mongodb://localhost:27017/')
                            destination_client = pymongo.MongoClient('mongodb://localhost:27017/') 

                            if self.EltAChanger['Base']=='Hypnose_documents_en_attente':
                                source_collect = source_client[str(self.Ancienne_bases)]
                                destination_collect = destination_client['Hypnose_documents_en_attente']
                            elif self.EltAChanger['Base']=='Hypnose_documents_validés':
                                source_collect = source_client[str(self.Ancienne_bases)]
                                destination_collect = destination_client['Hypnose_documents_validés']

                     # ON NE CHANGE PAS DE STORAGE ET ON NE CHANGE PAS DE BASE
                    elif  self.changebase_var.get()==0: # Supposons que la base de stockage ne change pas 

                        # Si la destination est le cloud
                        if self.EltAChanger['Storage']=='Cloud': # On configure la Storage de données pour se connecter
                            source_client = pymongo.MongoClient('mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/')
                            destination_client = pymongo.MongoClient('mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/') 

                            if self.EltAChanger['Base']=='Hypnose_documents_en_attente':
                                source_collect = source_client['Hypnose_documents_en_attente']
                                destination_collect = destination_client['Hypnose_documents_en_attente']
                            elif self.EltAChanger['Base']=='Hypnose_documents_validés':
                                source_collect = source_client['Hypnose_documents_validés']
                                destination_collect = destination_client['Hypnose_documents_validés'] 

                        # Si la destinatination est le local
                        elif self.EltAChanger['Storage']=='Locale': # On configure la Storage de données pour se connecter
                            source_client = pymongo.MongoClient('mongodb://localhost:27017/')
                            destination_client = pymongo.MongoClient('mongodb://localhost:27017/') 

                            if self.EltAChanger['Base']=='Hypnose_documents_en_attente':
                                source_collect = source_client['Hypnose_documents_en_attente']
                                destination_collect = destination_client['Hypnose_documents_en_attente']
                            elif self.EltAChanger['Base']=='Hypnose_documents_validés':
                                source_collect = source_client['Hypnose_documents_validés']
                                destination_collect = destination_client['Hypnose_documents_validés']               
                
                
                # Récupérer les instances de GridFS               

                source_fs = GridFS(source_collect)
                destination_fs = GridFS(destination_collect)

                selected_item = self.tree.selection()
                if selected_item:
                    count_file=0
                    for item in selected_item:
                        # Récupérer l'index de chaque élément
                        # Récupérer les valeurs de chaque élément
                        #values = self.tree.item(item, 'values')
                        #id=values[6]
                        item_id = self.tree.item(item, 'text')
                        # Convertir l'ID en un objet ObjectId
                        object_id = ObjectId(item_id)
                        
                        file = source_fs.find_one({'_id': object_id})
                        filename = file.metadata.get('filename', 'N/A')
                        #file = source_fs.get(object_id_str)
                        
                        if file:
                            # Vérifier si un fichier avec le même nom existe déjà dans la Storage de données de destination
                            existing_file = destination_fs.find_one({'filename': filename})
                            if existing_file:
                                messagebox.showwarning("Warning", f"File '{filename}' already exists in the destination database.")
                            else:
                                # Copier le fichier vers la Storage de données destination
                                destination_fs.put(file.read(), metadata=file.metadata)
                                # Supprimer le fichier de la Storage de données source
                                source_fs.delete(object_id)
                                # Supprimer l'élément du Treeview
                                self.tree.delete(item)
                                count_file+=1
                                # On actualise la barre de progression
                                self.progress_bar['value'] = (count_file / len(selected_item)) * 100                               
                                self.progress_bar.update()
                  
                        else:
                            messagebox.showwarning("Warning", f"File with ID {filename} not found.")

                # Fermer les connexions
                self.progress_bar.stop()
                # Délection les checkboxes sélectionnés

                if self.changestorage_var.get() == 1:  # Si la case à cocher est cochée
                   self.changestorage_var.set(0) 
                if self.changebase_var.get() == 1:  # Si la case à cocher est cochée
                   self.changebase_var.set(0) 
                
                self.changercollection()
                self.changerbase()
                #self.Appel_loading_data()
                self.tree.update_idletasks() # On raffraichit notre treeview
                source_client.close()
                destination_client.close()
                

        except Exception as e:
            messagebox.showerror("Connexion", f"Erreur de connexion : {e}",parent=self.window)
        
    def ModifyorCreate(self):
        try:
            if self.basecloud_var.get() == 1:
                # Connexion à la Storage de données
                self.Client = pymongo.MongoClient("mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/")
                db=self.Client["Cloud"]
                self.EltAChanger['Storage']="Cloud" 

                if self.docattente_var.get() == 1 :
                    Base = db["Hypnose_documents_en_attente"]
                    self.EltAChanger['Base']="Hypnose_documents_en_attente" #On récupère la Base sélectionnée
                    # Récupération de tous les documents dans la Base
                    cursor = Base.find()
                    # Exemple d'utilisation pour vider le Treeview
                    self.clear_treeview()
                    # Insertion des données dans le Treeview
                    
                    for doc in cursor:
                        self.tree.insert('', 'end', values=(doc['Date'],doc['Titre'], doc['Auteur'],doc['Pages'],doc['Type'],doc['Langue'],doc['_id']))
                    
                    self.Client.close()

                elif self.docvalide_var.get() == 1 :
                    Base = db["Hypnose_documents_validés"]
                    self.EltAChanger['Base']="Hypnose_documents_validés" #On récupère la Base sélectionnée
                    # Récupération de tous les documents dans la Base
                    cursor = Base.find()
                    # Exemple d'utilisation pour vider le Treeview
                    self.clear_treeview()
                    # Insertion des données dans le Treeview
                    
                    for doc in cursor:
                        self.tree.insert('', 'end', values=(doc['Date'],doc['Titre'], doc['Auteur'],doc['Pages'],doc['Type'],doc['Langue'],doc['_id']))
                    
                    self.Client.close()
                else:
                    messagebox.showerror("Affichage", "Aucune table n'a été sélectionnée.")
                                      
            elif self.baselocale_var.get() == 1 :
                # Connexion à la Storage de données
                self.Client = pymongo.MongoClient("mongodb://localhost:27017/")
                db=self.Client["Locale"]
                self.EltAChanger['Storage']="Locale" #On récupère la Storage sélectionnée

                if self.docattente_var.get() == 1 :
                    Base = db["Hypnose_documents_en_attente"]
                    self.EltAChanger['Base']="Hypnose_documents_en_attente" #On récupère la Base sélectionnée
                    # Récupération de tous les documents dans la Base
                    cursor = Base.find()
                    # Exemple d'utilisation pour vider le Treeview
                    self.clear_treeview()
                    # Insertion des données dans le Treeview
                    
                    for doc in cursor:
                        self.tree.insert('', 'end', values=(doc['Date'],doc['Titre'], doc['Auteur'],doc['Pages'],doc['Type'],doc['Langue'],doc['_id']))
                    
                    self.Client.close()

                elif self.docvalide_var.get() == 1 :
                    Base = db["Hypnose_documents_validés"]
                    self.EltAChanger['Base']="Hypnose_documents_validés" #On récupère la Base sélectionnée
                    # Récupération de tous les documents dans la Base
                    cursor = Base.find()
                    # Exemple d'utilisation pour vider le Treeview
                    self.clear_treeview()
                    
                    # Insertion des données dans le Treeview
                    for doc in cursor:
                        self.tree.insert('', 'end', values=(doc['Date'],doc['Titre'], doc['Auteur'],doc['Pages'],doc['Type'],doc['Langue'],doc['_id']))
                   
                    self.Client.close()
                else:
                    messagebox.showerror("Affichage", "Aucune table n'a été sélectionnée.")
                     
            else:
                messagebox.showerror("Affichage", "Aucune Storage n'a été sélectionnée.")
                 
        except Exception as e:
            messagebox.showerror("Connexion", f"Erreur lors du chargement des données : {e}",parent=self.window)
                
    def clear_treeview(self):
        # Supprimer toutes les lignes du Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

    def remove_file(self):
        # Connexion à la Storage de données
        if self.EltAChanger['Storage']=="Cloud" :
            Client = pymongo.MongoClient("mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/")
            db=Client[self.EltAChanger['Base']]
        elif self.EltAChanger['Storage']=="Locale":
            Client = pymongo.MongoClient("mongodb://localhost:27017/")
            db=Client[self.EltAChanger['Base']]
       
        # Récupérer l'élément sélectionné dans le Treeview
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un fichier à supprimer.")
            return
        else:

            if messagebox.askyesno("Avertissement", "Voulez-vous supprimer ces fichiers de votre base ?",parent=self.window) :                                            
                fs = GridFS(db)                        

                for item in selected_items :       
                    # Récupérer l'ID de l'élément sélectionné
                    item_id = self.tree.item(item, 'text')
                    #Transformer l'id en objectID
                    object_id = ObjectId(item_id)
                    # Suppression de l'élément dans GridFS
                    fs.delete(object_id) 
                    # Supprimer l'élément du Treeview
                    self.tree.delete(item) 
        Client.close()

#if __name__ == "__main__":
    #app = UserF()
    #app.window.mainloop()


#if __name__ == "__main__":
    #root = tk.Tk()
    #login_window = Login(root)
    #root.mainloop()