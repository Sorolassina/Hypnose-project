import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
import datetime
import PyPDF2
import pymongo
import os
from tkinter import messagebox, simpledialog
from langdetect import detect
import fitz  # PyMuPDF
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hypnose Manager file")
        self.root.iconbitmap('logo2.ico')

        self.window_width = 1380
        self.window_height = 450
        self.center_window()
       
        self.tree = Treeview(root, columns=('Date', 'Titre', 'Auteur', 'Pages', 'Type', 'Langue','Contenu'))
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
        self.titrebar_label = ttk.Label(root, text="", font=("Arial", 8),width=1380)
        self.titrebar_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=1380, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        btn_select_files = tk.Button(root, text="Sélectionner des fichiers", command=self.select_files, cursor="hand2",width=35)
        btn_select_files.pack(pady=10)
        
        btn_process_files = tk.Button(root, text="Charger dans la base", command=self.load_to_database, cursor="hand2",width=35)
        btn_process_files.pack(pady=5)

        btn_remove_file = tk.Button(root, text="Supprimer", command=self.remove_file, cursor="hand2",width=35)
        btn_remove_file.pack(pady=5)

    def load_to_database(self):
        # Connexion à la base de données MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Hypnose_base"]
        collection = db["Docs en attente"]

        
        processed_files = 0
        # Parcourir tous les éléments du Treeview
        for item in self.tree.get_children():
            # Récupérer les valeurs de chaque élément
            #title = self.tree.item(item, 'text')
            total_files = len(self.tree.get_children())
            values = self.tree.item(item, 'values')

            # Vérification si le document existe déjà dans la base de données
            if collection.find_one({"Titre": values[1],"Auteur": values[2]}):
                messagebox.showinfo("Info", f"Le document '{values[1]}' existe déjà dans la base de données.")
                continue

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
            collection.insert_one(document)

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
        

    def remove_file(self):
        # Récupérer l'élément sélectionné dans le Treeview
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un fichier à supprimer.")
        else:

            if messagebox.askyesno("Avertissement", "Voulez-vous supprimer ces fichier des documents à charger ?") :              
                # Supprimer chaque élément sélectionné du Treeview
                for item in selected_items:
                    # Supprimer l'élément du Treeview
                    self.tree.delete(item)

    def select_files(self):
        processed_files = 0 # On réinitilise le nombre de fichier
        filenames = filedialog.askopenfilenames(filetypes=[("Fichiers PDF", "*.pdf"),("Fichiers PDF", "*.csv")])

        for filename in filenames:
            Titre=filename.split("/")[-1] # On détermine le nom du document
            Type=Titre.split(".")[-1] # On détermine le type de document

            pdf_reader = PyPDF2.PdfReader(filename)

            total_files = len(filenames)
            # On extrait le contenu du document
            text = ""
            Nbrepages=0
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                Nbrepages+=page_num+1

            try: # On va déterminer ensuite la langue du documents
                language = detect(text)
            except:
                language="Langue non détectée"

            infos_doc = self.extract_metadata(filename) #simpledialog.askstring(Titre, "Quel est l'auteur de ce livre ? :",parent=self.root)
            #Title = self.extract_metadata(filename)
            self.tree.insert('', 'end', text=filename, values=(datetime.date.today(), infos_doc['Title'], infos_doc['Author'], Nbrepages, Type, language,text))

            # Mettre à jour la barre de progression et le label
            processed_files += 1
            self.progress_bar['value'] = (processed_files / total_files) * 100
            self.titrebar_label.config(text=f"Traitement du fichier : {infos_doc['Title']} de {infos_doc['Author']}")
            self.progress_bar.update()
            
        
        # Réinitialiser la barre de progression et le label une fois tous les fichiers traités
        self.progress_bar['value'] = 0
        self.titrebar_label.config(text="")

    def extract_metadata(self,file):
        metadata = {}
        pdf_document = fitz.open(file)
        
        metadata['Title'] = pdf_document.metadata.get('title', '')
        metadata['Author'] = pdf_document.metadata.get('author', '')
        metadata['Subject'] = pdf_document.metadata.get('subject', '')
        metadata['Producer'] = pdf_document.metadata.get('producer', '')
        metadata['CreationDate'] = pdf_document.metadata.get('creationDate', '')
        metadata['ModificationDate'] = pdf_document.metadata.get('modDate', '')

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
    root = tk.Tk()
    app = App(root)
    root.mainloop()
