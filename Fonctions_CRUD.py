import pymysql
import pymongo
import os
from tkinter import filedialog
import tkinter as tk

# Fonction pour se connecter à la base de données SQL
def connectSQL():
    try:
        conn = pymysql.connector.connect(
            host="localhost",
            user="votre_utilisateur",
            password="votre_mot_de_passe",
            database="nom_de_votre_base_de_donnees"
        )
        return conn
    except Exception as e:
        print(f"Erreur lors de la connexion à SQL : {e}")
        return None

# Fonction pour se connecter à la base de données MONGODB
def connect_mongodb():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["cars"]
        return db
    except Exception as e:
        print(f"Erreur lors de la connexion à MongoDB : {e}")
        return None
                           

# Fonction pour lire un enregistrement dans la base de données
def display_record(id, db_type,table):
    if db_type == "mongodb":
        db = connect_mongodb()
        if db is not None:
            collection = db[table]
            result = collection.find_one({"name": id})
            print("Enregistrement trouvé dans MongoDB :", result)
    elif db_type == "sql":
        conn = connectSQL()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM users WHERE email = %s", (id,))
                result = cursor.fetchone()
                print("Enregistrement trouvé dans SQL :", result)
            except Exception as e:
                print(f"Erreur lors de la lecture de l'enregistrement dans SQL : {e}")
            finally:
                cursor.close()
                conn.close()
    else:
        print("Type de base de données non pris en charge.")


def charger_fichier(Base_type, Nom_base, collect=0):
    # Connexion à la base de données MySQL
    conn = connectSQL()
    cursor = conn.cursor()

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
                    cursor.execute("INSERT INTO fichiers (titre, type, contenu) VALUES (%s, %s, %s)", (nom, extension, contenu))                   
                    print("Fichier chargé avec succès :", nom_fichier)

            # Valider la transaction
            conn.commit()

    except pymysql.Error as e:
        print("Erreur lors du chargement des fichiers :", e)

    finally:
        # Fermer le curseur et la connexion
        cursor.close()
        conn.close()

import tempfile
import webbrowser

def lire_fichier(id):
        # Connexion à la base de données
        conn = connectSQL()
        cursor = conn.cursor()

        try:
            # Exécuter une requête SQL pour obtenir le contenu du fichier à partir de la base de données
            cursor.execute("SELECT contenu FROM fichiers WHERE id = %s", (id))
            row = cursor.fetchone()

            if row:  # Vérifier si le fichier existe
                contenu = row[0]  # Récupérer le contenu du fichier

                # Convertir le contenu binaire en chaîne de caractères avec l'encodage UTF-8
                contenu_texte = contenu.decode("latin-1")

                # Créer un fichier temporaire HTML avec le contenu du fichier
                with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp_file:
                    temp_file.write(contenu_texte.encode("latin-1"))

                # Ouvrir le fichier temporaire dans un navigateur Web
                webbrowser.open("file://" + temp_file.name)

        except pymysql.Error as e:
            print("Erreur lors de la lecture du fichier :", e)

        finally:
            # Fermer le curseur et la connexion
            cursor.close()
            conn.close()
    

# Fonction pour créer un enregistrement dans la base de données
def create_record(nom, prenoms, email, question, reponse, mot_de_passe):
    conn = connectSQL()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (nom, prenoms, email, question, reponse, mot_de_passe) VALUES (%s, %s, %s, %s, %s, %s)",
                       (nom, prenoms, email, question, reponse, mot_de_passe))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la création de l'enregistrement : {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()



# Fonction pour lire tous les enregistrements dans la base de données
def display_recordall():
    conn = connectSQL()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la lecture de l'enregistrement : {e}")
    finally:
        cursor.close()
        conn.close()

# Fonction pour mettre à jour un enregistrement dans la base de données
def update_record(email, new_email):
    conn = connectSQL()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET email=%s WHERE email=%s", (new_email, email))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'enregistrement : {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Fonction pour supprimer un enregistrement dans la base de données
def delete_record(email):
    conn = connectSQL()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE email=%s", email)
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la suppression de l'enregistrement : {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
