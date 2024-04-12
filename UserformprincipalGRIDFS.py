from pymongo import MongoClient
from gridfs import GridFS

# Se connecter à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Test_hypnose']

# Créer une instance GridFS
fs = GridFS(db)

# Ouvrir et lire le fichier PDF
with open('F31PME.pdf', 'rb') as pdf_file:
    # Enregistrer le fichier PDF dans GridFS
    file_id = fs.put(pdf_file, filename='F31PME.pdf')

print("PDF file saved with ID:", file_id)
