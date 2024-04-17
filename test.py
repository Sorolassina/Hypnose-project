""" def Stockage_Gridfs (self, db, pdf_file_path, doc):
        # Se connecter à MongoDB
        print (doc)
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
            file_id = fs.put(pdf_file, metadata=metadata) """


""" # Récupérez le premier élément sélectionné
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
            date_obj = datetime.strptime(values[0], "%Y-%m-%d")
            self.de_entry.set_date(date_obj.strftime("%d-%m-%Y"))
            
            self.title_entry.insert(0,values[1])          
            self.aut_entry.insert(0,values[2])
            self.page_entry.insert(0,values[3])
            self.type_entry.set(values[4])
            self.langue_entry.set(values[5])
            self.EltAChanger['Id']=values[6]
        
            
        else:
            
            # Effacer les valeurs si aucun élément n'est sélectionné
            self.title_entry.delete(0,END)
            self.aut_entry.delete(0,END)
            self.page_entry.delete(0,END)
            self.type_entry.set("")
            self.langue_entry.set("")
 """