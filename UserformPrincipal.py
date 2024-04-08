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

class UserF():
    def __init__(self):
        self.window=Tk()     
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
  
        # Cadre où afficher les données de ma base de données
        # Définition du style pour la couleur de fond du cadre
        self.style = ttk.Style()
        self.style.configure('My.TFrame', background='#FFFFFF')  # Couleur de fond grise
        # Création du cadre avec une bordure et une couleur de fond
        Cadre_affichage = ttk.Frame(zone1, borderwidth=2, style='My.TFrame',relief='groove')
        Cadre_affichage.place(x=310,y=55,width=815,height=655)
         
         # Création du Treeview avec 3 colonnes
        self.tree = ttk.Treeview(Cadre_affichage, columns=("Date",'Titre','Auteur','Pages','Type','Langue'))
        
        # Définition des en-têtes de colonnes
        self.tree.heading("Date", text="Date")
        self.tree.heading('Titre', text='Titre')
        self.tree.heading('Auteur', text='Auteur')      
        self.tree.heading("Pages", text="Pages")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Langue", text="Langue")
        
        self.tree["show"]="headings"

        # Définition de la largeur des colonnes
        #self.tree.column('id',width=100)
        self.tree.column("Date", width=70)
        self.tree.column('Titre', width=150)
        self.tree.column('Auteur', width=150)
        self.tree.column("Pages", width=50)
        self.tree.column("Type", width=150)
        self.tree.column("Langue", width=100)
        
        self.tree.pack(expand=True,fill='both')
        self.tree.bind("<ButtonRelease-1")

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

        # Création du cadre pour les box à renseigner
        Cadre_box = ttk.Frame(zone1, borderwidth=2, style='My.TFrame',relief='groove')
        Cadre_box.place(x=20,y=20,width=280,height=690)
          
            # Titre 
        self.title_label = ttk.Label(Cadre_box, text="Titre", font=myFontLabel,width=20,background="white")
        self.title_label.place(x=15, y=15)
        self.title_entry = Entry(Cadre_box, background='#FFFFFF')
        self.title_entry.place(x=15, y=45,width=200,height=25) 

            # Auteur 
        self.aut_label = ttk.Label(Cadre_box, text="Auteur", font=myFontLabel,width=20,background="white")
        self.aut_label.place(x=15, y=75)
        self.aut_entry = Entry(Cadre_box, background='#FFFFFF')
        self.aut_entry.place(x=15, y=105,width=200,height=25) 
  
            # Date enregistrement 
        self.de_label = ttk.Label(Cadre_box, text="Date", font=myFontLabel,width=20,background="white")
        self.de_label.place(x=15, y=135)
        self.de_entry = DateEntry(Cadre_box, background='#FFFFFF')
        self.de_entry.place(x=15, y=165,width=200,height=25)

            # Nombre de page 
        self.page_label = ttk.Label(Cadre_box, text="Pages", font=myFontLabel,width=20,background="white")
        self.page_label.place(x=15, y=195)
        self.page_entry = Entry(Cadre_box, background='#FFFFFF')
        self.page_entry.place(x=15, y=225,width=200,height=25) 
        
            # Genre
        self.genre_label = ttk.Label(Cadre_box, text="Type", font=myFontLabel,width=20,background="white")
        self.genre_label.place(x=15, y=255)
        self.type_entry = ttk.Combobox(Cadre_box, background='#FFFFFF',values=("pdf","csv","text","docx"))
        self.type_entry.place(x=15, y=285,width=200,height=25) 

         # Langues
        self.langue_label = ttk.Label(Cadre_box, text="Langue", font=myFontLabel,width=20,background="white")
        self.langue_label.place(x=15, y=315)
        self.langue_entry = ttk.Combobox(Cadre_box, background='#FFFFFF',values=("fr","en","de","es","pt"))
        self.langue_entry.place(x=15, y=345,width=200,height=25) 

        # Création du cadre pour les boutons
        Cadre_bouton = ttk.Frame(zone1, borderwidth=2, style='My.TFrame',relief="solid")
        Cadre_bouton.place(x=1120,y=20,width=190,height=690)

            # Boutons de CRUD
        # Créez la case à cocher
        # Créez un style personnalisé pour la case à cocher
        self.styleck = ttk.Style()
        self.styleck.configure("White.TCheckbutton", background="white",borderwidth=0,foreground="green")
        # Créez une variable Tkinter pour stocker l'état de la case à cocher
        self.etat_checkbox = tk.IntVar()
        self.checkbox = ttk.Checkbutton(Cadre_bouton, text="Documents validés",style="White.TCheckbutton", cursor="hand2",variable=self.etat_checkbox, command=self.etat_modifie)
        self.checkbox.place(x=8,y=20)

        #refresh_button = Button(Cadre_bouton, width=20,text="Actualiser",font=myFontBouton, command="",cursor="hand2").place(x=8, y=50)
        create_button = Button(zone1, width=15,text="Charger fichiers",font=myFontBouton, command=self.loading_file,cursor="hand2")
        create_button.place(x=970, y=20)    
        update_button = Button(Cadre_box, width=10,text="Enregistrer",font=myFontBouton, command="",cursor="hand2").place(x=15, y=375)
        delete_button = Button(Cadre_box, width=10,text="Supprimer",font=myFontBouton, command="",cursor="hand2").place(x=110, y=375)
        quit_button = Button(Cadre_bouton, width=20,text="Quitter",bg="red",foreground="white",font=myFontBouton, command="",cursor="hand2").place(x=8, y=450)

        self.lookvalue_entry = ttk.Entry(zone1, background='#FFFFFF')
        self.lookvalue_entry.place(x=310, y=20,width=500,height=28) 
        self.lookvalue_entry.bind("<KeyRelease>", self.filter_tree)

        look_button = Button(zone1, width=15,text="Rechercher",foreground="black",font=myFontBouton, command="",cursor="hand2")      
        look_button.place(x=825, y=20)  
        # Récupération des données depuis la base de données MongoDB
        self.load_dataDV()
        # On va centre toutes les données de ma tree view pour un meilleur affichage
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")

    def loading_file(self):
        app = App(self.window) 
    
    def etat_modifie(self):
        # Fonction de rappel pour exécuter lorsque la case à cocher est cochée ou décochée
        if self.etat_checkbox.get() == 1:
            self.styleck.configure("White.TCheckbutton", background="white",borderwidth=0,foreground="red")
            self.checkbox.configure(text="Documents en attente",style="White.TCheckbutton")
            self.tree.delete(*self.tree.get_children())
            self.load_dataDEA()
        else:
            self.styleck.configure("White.TCheckbutton", background="white",borderwidth=0,foreground="green")
            self.checkbox.configure(text="Documents validés")
            self.tree.delete(*self.tree.get_children())
            self.load_dataDV()

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
            # Récupérez le premier élément sélectionné
            first_selected_item = selected_items[0]
            # Récupérez les valeurs de chaque colonne pour le premier élément sélectionné
            values = event.widget.item(first_selected_item, 'values')
            
            # Réinitialisation des box
            self.title_entry.delete(0,END)
            self.aut_entry.delete(0,END)
            self.page_entry.delete(0,END)
            self.type_entry.set("")
            self.langue_entry.set("")

            # Affichez les valeurs récupérées
            
            self.de_entry.set_date(datetime.strptime(values[0], '%Y-%m-%d'))
            self.title_entry.insert(0,values[1])          
            self.aut_entry.insert(0,values[2])
            self.page_entry.insert(0,values[3])
            self.type_entry.set(values[4])
            self.langue_entry.set(values[5])

        else:
            
            # Pour insérer la date du jour si aucun élément n'est sélectionné
            today = datetime.date.today()
            self.de_entry.set_date(today)

            # Effacer les valeurs si aucun élément n'est sélectionné
            self.title_entry.delete(0,END)
            self.aut_entry.delete(0,END)
            self.page_entry.delete(0,END)
            self.type_entry.set("")
            self.langue_entry.set("")

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

    def load_dataDEA(self):
        try:
            # Connexion à la base de données
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["Hypnose_base"]
            collection = db["Docs en attente"]

            # Récupération de tous les documents dans la collection
            cursor = collection.find()

            # Insertion des données dans le Treeview
            for doc in cursor:
                self.tree.insert('', 'end', values=(doc['Date'],doc['Titre'], doc['Auteur'],doc['Pages'],doc['Type'],doc['Langue']))

            client.close()

        except Exception as e:
            messagebox.showerror("Connexion", f"Erreur lors du chargement des données : {e}",parent=self.root)
    
    def load_dataDV(self):
        try:
            # Connexion à la base de données
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["Hypnose_base"]
            collection = db["Docs validés"]

            # Récupération de tous les documents dans la collection
            cursor = collection.find()

            # Insertion des données dans le Treeview
            for doc in cursor:
                self.tree.insert('', 'end', values=(doc['Date'],doc['Titre'], doc['Auteur'],doc['Pages'],doc['Type'],doc['Langue']))

            client.close()

        except Exception as e:
            messagebox.showerror("Connexion", f"Erreur lors du chargement des données : {e}",parent=self.root)

if __name__ == "__main__":
    app = UserF()
    app.window.mainloop()
