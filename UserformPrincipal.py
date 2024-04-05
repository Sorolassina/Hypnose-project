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
         
        # Configuration des scrollbars
        yscroll = ttk.Scrollbar(Cadre_affichage, orient='vertical')
        xscroll = ttk.Scrollbar(Cadre_affichage, orient='horizontal')

        # Position d'affichage des scrollbars
        xscroll.pack(side=BOTTOM,fill=X)
        yscroll.pack(side=RIGHT,fill=Y)

         # Création du Treeview avec 3 colonnes
        self.tree = ttk.Treeview(Cadre_affichage, columns=("créé",'titre','auteur','nombre de page','genre','langue'),xscrollcommand=xscroll.set,yscrollcommand=yscroll.set)
        
        # Définition des en-têtes de colonnes
        #self.tree.heading('id', text='Id')
        self.tree.heading("créé", text="Créé le")
        self.tree.heading('titre', text='Titre')
        self.tree.heading('auteur', text='Auteur')      
        self.tree.heading("nombre de page", text="Pages")
        self.tree.heading("genre", text="Genre")
        self.tree.heading("langue", text="Langue")
        
        self.tree["show"]="headings"

        # Définition de la largeur des colonnes
        #self.tree.column('id',width=100)
        self.tree.column("créé", width=70)
        self.tree.column('titre', width=150)
        self.tree.column('auteur', width=150)
        self.tree.column("nombre de page", width=50)
        self.tree.column("genre", width=150)
        self.tree.column("langue", width=100)
        
        self.tree.pack(expand=True,fill='both')
        self.tree.bind("<ButtonRelease-1")
        # Lier la fonction à l'événement <<TreeviewSelect>>
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)
        xscroll.bind("<B1-Motion>", lambda event: self.tree.xview_moveto(event.x))
        yscroll.bind("<B1-Motion>", lambda event: self.tree.yview_moveto(event.y))

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
        self.de_label = ttk.Label(Cadre_box, text="Date enregistrement", font=myFontLabel,width=20,background="white")
        self.de_label.place(x=15, y=135)
        self.de_entry = DateEntry(Cadre_box, background='#FFFFFF')
        self.de_entry.place(x=15, y=165,width=200,height=25)

            # Nombre de page 
        self.page_label = ttk.Label(Cadre_box, text="Nombre de page", font=myFontLabel,width=20,background="white")
        self.page_label.place(x=15, y=195)
        self.page_entry = Entry(Cadre_box, background='#FFFFFF')
        self.page_entry.place(x=15, y=225,width=200,height=25) 
        
            # Genre
        self.genre_label = ttk.Label(Cadre_box, text="Genre", font=myFontLabel,width=20,background="white")
        self.genre_label.place(x=15, y=255)
        self.genre_entry = ttk.Combobox(Cadre_box, background='#FFFFFF',values=("Roman policier","Littérature fantastique","Science-fiction","Essais","Biographies","Romans d’aventure","Littérature cyberpunk","Récits de voyage","Romans graphiques","Rapports","Autres"))
        self.genre_entry.place(x=15, y=285,width=200,height=25) 

         # Langues
        self.langue_label = ttk.Label(Cadre_box, text="Langue", font=myFontLabel,width=20,background="white")
        self.langue_label.place(x=15, y=315)
        self.langue_entry = ttk.Combobox(Cadre_box, background='#FFFFFF',values=("Français","Anglais","Allemand","Espagnole","Portugais"))
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
        create_button = Button(zone1, width=15,text="Charger un fichier",font=myFontBouton, command="",cursor="hand2")
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
            if filter_text in self.tree.item(item)['text'].lower():
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
            #print(values[0],values[1],values[2],values[3],values[4],values[5])
            # Réinitialisation des box
            self.title_entry.delete(0,END)
            self.aut_entry.delete(0,END)
            self.page_entry.delete(0,END)
            self.genre_entry.set("")
            self.langue_entry.set("")

            # Affichez les valeurs récupérées
            self.de_entry.set_date(values[0])
            self.title_entry.insert(0,values[1])          
            self.aut_entry.insert(0,values[2])
            self.page_entry.insert(0,values[3])
            self.genre_entry.set(values[4])
            self.langue_entry.set(values[5])

        else:
            
            # Pour insérer la date du jour si aucun élément n'est sélectionné
            today = datetime.date.today()
            self.de_entry.set_date(today)

            # Effacer les valeurs si aucun élément n'est sélectionné
            self.title_entry.delete(0,END)
            self.aut_entry.delete(0,END)
            self.page_entry.delete(0,END)
            self.genre_entry.set("")
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
                self.tree.insert('', 'end', values=(doc['créé'],doc['titre'], doc['auteur'],doc['nombre de page'],doc['genre'],doc['langue']))

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
                self.tree.insert('', 'end', values=(doc['créé'],doc['titre'], doc['auteur'],doc['nombre de page'],doc['genre'],doc['langue']))

            client.close()

        except Exception as e:
            messagebox.showerror("Connexion", f"Erreur lors du chargement des données : {e}",parent=self.root)

if __name__ == "__main__":
    app = UserF()
    app.window.mainloop()
