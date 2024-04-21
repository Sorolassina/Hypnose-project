import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
import datetime
import PyPDF2
import pymongo
from tkinter import messagebox, simpledialog
from langdetect import detect
import fitz  # PyMuPDF
from tkinter import ttk
from tkinter import *
from gridfs import GridFS
import os
import pdfplumber

class App():
    def __init__(self, master=None):
        self.master=master
        self.root = Toplevel(self.master)
        self.root.title("Hypnose Manager file")
        self.root.iconbitmap('logo2.ico')

        self.window_width = 1380
        self.window_height = 450
        self.center_window()
       
        self.tree = Treeview(self.root, columns=('Date', 'Titre', 'Auteur', 'Pages', 'Type', 'Langue','Contenu'))
        self.tree.heading('#0', text='Chemin')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Titre', text='Titre')
        self.tree.heading('Auteur', text='Auteur')
        self.tree.heading('Pages', text='Pages')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Langue', text='Langue')
        self.tree.heading('Contenu', text='Contenu')

        self.tree.pack(fill='both', expand=True)

        self.tree.column("Date", width=70)
        self.tree.column("Titre", width=70)
        self.tree.column("Auteur", width=70)
        self.tree.column("Pages", width=70)
        self.tree.column("Type", width=70)
        self.tree.column("Langue", width=70)
        self.tree.column("Contenu", width=70)

        # Création de la barre de progression avec une hauteur personnalisée en modifiant la taille de la police
        self.titrebar_label = ttk.Label(self.root, text="", font=("Arial", 8),width=1380)
        self.titrebar_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=1380, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        btn_select_files = tk.Button(self.root, text="Sélectionner des fichiers", command=self.select_files, cursor="hand2",width=35)
        btn_select_files.pack(pady=10)
        
        self.btn_process_files = tk.Button(self.root, text="Charger dans la base", command=self.Appel_loading_data, cursor="hand2",width=35,state='disabled')
        self.btn_process_files.pack(pady=5)

        btn_remove_file = tk.Button(self.root, text="Supprimer", command=self.remove_file, cursor="hand2",width=35)
        btn_remove_file.pack(pady=5)

        self.basecloud_var = tk.IntVar()
        self.checkbox_basecloud = ttk.Checkbutton(self.root, text="Stockage cloud", cursor="hand2",variable=self.basecloud_var,command=self.upload_button)
        self.checkbox_basecloud.place(x=855,y=345)

        self.baselocale_var = tk.IntVar()
        self.checkbox_baseclocale = ttk.Checkbutton(self.root, text="Stockage local", cursor="hand2",variable=self.baselocale_var,command=self.upload_button)
        self.checkbox_baseclocale.place(x=855,y=370)

        self.docattente_var = tk.IntVar()
        self.checkbox_docattente = ttk.Checkbutton(self.root, text="Mettre en attente les documents stockés", cursor="hand2",variable=self.docattente_var,command=self.upload_button)
        self.checkbox_docattente.place(x=1050,y=345)

        self.docvalide_var = tk.IntVar()
        self.checkbox_docvalide = ttk.Checkbutton(self.root, text="Marquer ces documents comme certifiés", cursor="hand2",variable=self.docvalide_var,command=self.upload_button)
        self.checkbox_docvalide.place(x=1050,y=370)

        # Bloquer le focus sur la fenêtre popup
        self.root.grab_set()

    def upload_button (self):

        self.CheckBoxDB_manage()
        self.CheckBoxCollect_manage()

        if self.basecloud_var.get() == 1 and self.docvalide_var.get() == 1:
           self.btn_process_files.config(state="normal")   
        elif self.baselocale_var.get() == 1 and self.docvalide_var.get() == 1:
           self.btn_process_files.config(state="normal")   
        elif self.baselocale_var.get() == 1 and self.docattente_var.get() == 1:
           self.btn_process_files.config(state="normal")  
        elif self.basecloud_var.get() == 1 and self.docattente_var.get() == 1:
           self.btn_process_files.config(state="normal")
        else :
            self.btn_process_files.config(state="disabled")  
    
    def CheckBoxDB_manage(self):
    # Fonction de rappel pour exécuter lorsque la case à cocher est cochée ou décochée

        if self.basecloud_var.get() == 1 and self.baselocale_var.get() == 0 :           
            self.checkbox_baseclocale.config(state="disabled")

        elif self.baselocale_var.get() == 1 and self.basecloud_var.get() == 0  :           
            self.checkbox_basecloud.config(state="disabled")

        elif self.basecloud_var.get() == 0 and self.baselocale_var.get() == 0 :           
            self.checkbox_baseclocale.config(state="normal")
            self.checkbox_basecloud.config(state="normal")

    def CheckBoxCollect_manage(self):
    # Fonction de rappel pour exécuter lorsque la case à cocher est cochée ou décochée
        if self.docvalide_var.get() == 1 and self.docattente_var.get() == 0 :           
            self.checkbox_docattente.config(state="disabled")

        elif self.docattente_var.get() == 1 and self.docvalide_var.get() == 0  :           
            self.checkbox_docvalide.config(state="disabled")
       
        elif self.docvalide_var.get() == 0 and self.docattente_var.get() == 0 :           
            self.checkbox_docattente.config(state="normal")
            self.checkbox_docvalide.config(state="normal")
   
    def Appel_loading_data(self) :
        if self.basecloud_var.get() == 1 and self.docvalide_var.get() == 1:      
           self.load_to_database()
        elif self.baselocale_var.get() == 1 and self.docvalide_var.get() == 1:      
           self.load_to_database()
        elif self.baselocale_var.get() == 1 and self.docattente_var.get() == 1:     
           self.load_to_database()
        elif self.basecloud_var.get() == 1 and self.docattente_var.get() == 1:
           self.load_to_database()
        else :
           messagebox.showinfo("Upload", "Merci de sélectionner une collection dans votre base cloud.")
 
    def load_to_database(self):
        # Connexion à la base de données MongoDB
        if self.basecloud_var.get() == 1  :
            client = pymongo.MongoClient("mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/")
            
            if self.docvalide_var.get() == 1:
                db = client["Hypnose_documents_validés"]
                #collection = db["Docs validés"]
            elif self.docattente_var.get() == 1:
                db = client["Hypnose_documents_en_attente"]
                #collection = db["Docs en attente"]
            else:
                messagebox.showinfo("Upload", "Merci de sélectionner une collection dans votre cloud.")
                return

        elif self.baselocale_var.get() == 1 :
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            #db = client["Test_hypnose"]

            if self.docvalide_var.get() == 1:
                db = client["Hypnose_documents_validés"]
                #collection = db["Docs validés"]
            elif self.docattente_var.get() == 1:
                db = client["Hypnose_documents_en_attente"]
                #collection = db["Docs en attente"]
            else:
                messagebox.showinfo("Upload", "Merci de sélectionner une collection dans votre base cloud.")
                return
        
        else :
            messagebox.showinfo("Upload", "Merci de sélectionner une base.")
            return

        processed_files = 0
        # Parcourir tous les éléments du Treeview
        for item in self.tree.get_children():
            # Récupérer les valeurs de chaque élément
            
            total_files = len(self.tree.get_children())
            values = self.tree.item(item, 'values')
            chemin = self.tree.item(item, 'text')
            
            # Vérification si le document existe déjà dans la base de données
            #if collection.find_one({"Titre": values[1],"Auteur": values[2]}):
                #messagebox.showinfo("Info", f"Le document '{values[1]}' existe déjà dans la base de données.")
                #continue

            # Insérer les valeurs dans la base de données
            document = {
                "Date": values[0],
                "Titre": values[1],
                "Auteur": values[2],
                "Pages": values[3],
                "Type": values[4],
                "Langue": values[5],
                "Contenu": values[6]
            }

            
            self.Stockage_Gridfs (db, chemin, document)

            processed_files += 1
            self.progress_bar['value'] = (processed_files / total_files) * 100
            self.titrebar_label.config(text=f"Insertion dans la base avec succès du document : {document['Titre']} de {document['Auteur']}")
            self.progress_bar.update()

        # Fermer la connexion à la base de données
        client.close()
        
        # Effacer le contenu du Treeview
        self.tree.delete(*self.tree.get_children())
        self.titrebar_label.config(text="")
        self.progress_bar['value'] = 0

        self.root.destroy()
        return
    

    def Stockage_Gridfs (self, db, pdf_file_path, doc):
        # Se connecter à MongoDB
        
        fs = GridFS(db)
        filename=pdf_file_path
        # Définir les métadonnées du fichier
        metadata = {
            'filename': filename.split("/")[-1],  # Nom du fichier
            'type': doc['Type'],  # Type de fichier
            'language': doc['Langue'],  # Langue du document
            'author': doc['Auteur'], 
            'pages': doc['Pages'],
            'contenu': doc['Contenu']
              
        }

        # Ouvrir le fichier PDF et le stocker dans GridFS avec les métadonnées
        with open(filename, 'rb') as pdf_file:
            file_id = fs.put(pdf_file, metadata=metadata)

    def remove_file(self):
        # Récupérer l'élément sélectionné dans le Treeview
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un fichier à supprimer.")
            return
        else:

            if messagebox.askyesno("Avertissement", "Voulez-vous supprimer ces fichier des documents à charger ?") :              
                # Supprimer chaque élément sélectionné du Treeview
                for item in selected_items:
                    # Supprimer l'élément du Treeview
                    self.tree.delete(item)

    def select_files(self):
        processed_files = 0 # On réinitilise le nombre de fichier
        filenames = filedialog.askopenfilenames(filetypes=[("Fichiers PDF", "*.pdf"),("Fichiers PDF", "*.csv")])

        # Bloquer le focus sur la fenêtre popup
        self.root.grab_set()
        files_issues=[]
        for filename in filenames:
            Titre=filename.split("/")[-1] # On détermine le nom du document
            Type=Titre.split(".")[-1] # On détermine le type de document

            #pdf_reader = PyPDF2.PdfReader(filename)
            pdf_reader = pdfplumber.open(filename)
            #pdf_reader = fitz.open(filename)

            total_files = len(filenames)
            # On extrait le contenu du document
            text = ""
            #Nbrepages=0
            infos_doc = self.extract_metadata(filename)
            for page_num in  range(len(pdf_reader.pages)):
                
                page = pdf_reader.pages[page_num]
                #page = pdf_reader.load_page(page_num)
                
                try: 
                    text += page.extract_text()
                    #text += page.extract_text()
                    #Nbrepages+=1
                except Exception as e:
                    files_issues.append(Titre)                   
                    messagebox.showwarning("Error",f"Erreur d'extraction de la page {page_num + 1}. L'erreur suivante empêche l'extraction : {e}")
                    break   

            try:
                language = detect(text) # On va déterminer ensuite la langue du documents               
            except Exception as e:
                language = "inconnue"
                    #messagebox.showwarning("Extraction",f"Error detecting language: {e}")
                   
            self.tree.insert('', 'end', text=filename, values=(datetime.date.today(), Titre, infos_doc['Author'], infos_doc['Nombrepage'], infos_doc['Format'], language,text))
            
             #simpledialog.askstring(Titre, "Quel est l'auteur de ce livre ? :",parent=self.root)
            #Title = self.extract_metadata(filename)
           
            # Mettre à jour la barre de progression et le label
            processed_files += 1
            self.progress_bar['value'] = (processed_files / total_files) * 100
            self.titrebar_label.config(text=f"Traitement du fichier : {Titre} de {infos_doc['Author']}")
            self.progress_bar.update()
                  
        # Réinitialiser la barre de progression et le label une fois tous les fichiers traités
        self.progress_bar['value'] = 0
        self.titrebar_label.config(text="")

        if len(files_issues)!=0:
            messagebox.showwarning("Fichiers non traités",f"les documents suivants n'ont pas été traités : {files_issues}")
    
    def extract_metadata(self,file):
        metadata = {}
        pdf_document = fitz.open(file)

        if pdf_document.metadata.get('title', '')=='':
           metadata['Title']="inconnue"
        else :
            metadata['Title'] = pdf_document.metadata.get('title', '')
        
        if pdf_document.metadata.get('author', '')=='':
          metadata['Author']="inconnue"
        else :
            metadata['Author'] = pdf_document.metadata.get('author', '')

        if pdf_document.metadata.get('subject', '')=='':
          metadata['Subject']="inconnue"
        else :
          metadata['Subject'] = pdf_document.metadata.get('subject', '')
        
        if pdf_document.metadata.get('producer', '')=='':
          metadata['Producer']="inconnue"
        else :
          metadata['Producer'] = pdf_document.metadata.get('producer', '')

        if pdf_document.metadata.get('creationDate', '')=='':
          metadata['CreationDate'] ="inconnue"
        else :
          metadata['CreationDate'] = pdf_document.metadata.get('creationDate', '')

        if pdf_document.metadata.get('modDate', '')=='':
          metadata['ModificationDate'] ="inconnue"
        else :
          metadata['ModificationDate'] = pdf_document.metadata.get('modDate', '')

        if pdf_document.metadata.get('format', '')=='':
          metadata['Format'] ="inconnue"
        else :
          metadata['Format'] = pdf_document.metadata.get('format', '')

        if pdf_document.page_count==0:
          metadata['Nombrepage'] ="inconnue"
        else :
          metadata['Nombrepage'] = pdf_document.page_count

        if pdf_document.language==None:
          metadata['Langue'] ="inconnue"
        else :
          metadata['Langue'] = pdf_document.language

        
        metadata['Crypte']=pdf_document.metadata.get('encryption', '')

        
        pdf_document.close()

        return metadata

    def count_pdf_pages(pdf_file_path):
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return reader.numPages
    
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    
if __name__ == "__main__":    
    app = App() # Capture le focus sur la fenêtre CreateLog
    app.root.mainloop()