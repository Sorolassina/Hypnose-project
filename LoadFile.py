import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
import datetime
import PyPDF2
import pymongo
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des fichiers PDF")
        self.root.iconbitmap('logo2.ico')

        self.window_width = 1300
        self.window_height = 750
        self.center_window()

        self.tree = Treeview(root, columns=('Titre', 'Auteur', 'Sortie', 'Créé', 'Genre', 'Langue'))
        self.tree.heading('#0', text='Nom du Fichier')
        self.tree.heading('Titre', text='Titre')
        self.tree.heading('Auteur', text='Auteur')
        self.tree.heading('Sortie', text='Sortie')
        self.tree.heading('Créé', text='Créé')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Langue', text='Langue')
        self.tree.pack(fill='both', expand=True)

        self.tree.column("Titre", width=70)
        self.tree.column("Auteur", width=70)
        self.tree.column("Sortie", width=70)
        self.tree.column("Créé", width=70)
        self.tree.column("Genre", width=70)
        self.tree.column("Langue", width=70)
        
        btn_select_files = tk.Button(root, text="Sélectionner des fichiers", command=self.select_files)
        btn_select_files.pack(pady=10)
        
        btn_process_files = tk.Button(root, text="Traiter les fichiers", command=self.process_files)
        btn_process_files.pack(pady=5)
        
    def select_files(self):
        filenames = filedialog.askopenfilenames(filetypes=[("Fichiers PDF", "*.pdf")])
        for filename in filenames:
            self.tree.insert('', 'end', text=filename, values=('Non Renseigné', 'Non Renseigné', 'Non Renseigné', datetime.date.today(), 'Non Renseigné', 'Non Renseigné'))



    def process_files(self):
        for child in self.tree.get_children():
            title = self.tree.item(child, 'text')
            messagebox.showinfo("Traitement", f"Traitement du fichier : {title}")

            # Extraction du contenu du PDF
            try:
                with open(title, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    num_pages = reader.numPages
                    text = ''
                    for page_num in range(num_pages):
                        page = reader.getPage(page_num)
                        text += page.extractText()
                    
                    # Vérification des valeurs manquantes
                    if not self.check_values(title, text):
                        messagebox.showwarning("Attention", "Certaines valeurs sont manquantes.")
                        continue

                    # Ici, vous pouvez ajouter le code pour mettre à jour les informations dans la base de données
                    # Par exemple, insérer le texte extrait dans une base de données MongoDB
                    # Pour l'exemple, affichons simplement le texte extrait dans une boîte de dialogue
                    messagebox.showinfo("Contenu extrait", f"Contenu du fichier '{title}':\n{text}")

            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite lors du traitement du fichier '{title}':\n{str(e)}")

    def check_values(self, title, text):
        # Vérifiez si les valeurs nécessaires sont présentes dans le texte extrait
        # Par exemple, vous pouvez rechercher des motifs dans le texte pour les valeurs manquantes
        # Si une valeur est manquante, demandez à l'utilisateur de la saisir
        if 'titre:' not in text.lower():
            new_title = messagebox.askstring("Valeur manquante", f"Entrez le titre pour le fichier '{title}':")
            if new_title:
                # Mettez à jour le titre avec la nouvelle valeur saisie
                title = new_title
            else:
                return False

        # Répétez cette vérification pour d'autres valeurs nécessaires comme l'auteur, la date, le genre, etc.

        return True

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def charger_fichier(Base_type, Nom_base, collect=0):
        # Connexion à la base de données MySQL
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Hypnose_base"]
        collection = db["Manage_Users"]
        

        try:
            # Ouvrir une boîte de dialogue pour sélectionner un ou plusieurs fichiers
            noms_fichiers = filedialog.askopenfilenames(title="Sélectionner des fichiers")

            # Vérifier si des fichiers ont été sélectionnés
            if noms_fichiers:
                # Parcourir chaque fichier sélectionné
                for nom_fichier in noms_fichiers:
                    # Vérifier si le fichier existe et est accessible
                    if not os.path.isfile(nom_fichier):
                        print("Le fichier spécifié n'existe pas ou n'est pas accessible :", nom_fichier)
                        continue

                    # Ouvrir le fichier en mode lecture binaire
                    with open(nom_fichier, 'rb') as file:
                        # Récupérer le nom de fichier et l'extension
                        nom, extension = os.path.splitext(nom_fichier)

                        # Vérifier si l'extension est vide (pas d'extension)
                        if not extension:
                            print("Le fichier n'a pas d'extension :", nom_fichier)
                            continue

                        # Charger le contenu du fichier dans une variable
                        contenu = file.read()

                        # Exécuter la requête SQL pour insérer le contenu du fichier dans la base de données
                        

                # Valider la transaction
                

        except pymongo.Error as e:
            print("Erreur lors du chargement des fichiers :", e)

        finally:
            # Fermer le curseur et la connexion
            client.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
