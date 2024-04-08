import tkinter as tk
from tkinter import scrolledtext
from transformers import CTRLTokenizer, CTRLLMHeadModel
import pymongo

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Génération de Texte")

        # Connexion à MongoDB Cloud
        self.client_cloud = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db_cloud = self.client_cloud["Hypnose_base"]

        # Création de l'index texte sur le champ "Contenu"
        self.db_cloud["Docs en attente"].create_index([("Contenu", "text")])

        # Chargement du tokenizer et du modèle CTRL
        self.tokenizer = CTRLTokenizer.from_pretrained("ctrl")
        self.model = CTRLLMHeadModel.from_pretrained("ctrl")

        # Création de l'interface utilisateur
        self.create_ui()

    def create_ui(self):
        self.chat_history = scrolledtext.ScrolledText(self.root, width=60, height=20)
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(self.root, text="Envoyer", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

    def search_database(self, user_message):
        self.db_cloud["Docs validés"].create_index([("Contenu", "text")])
        # Recherche dans la collection "Docs validés"
        cloud_result = self.db_cloud["Docs validés"].find_one({"$text": {"$search": user_message}})
        if cloud_result:
            return cloud_result["Contenu"]
        return None

    def generate_response(self, user_message):
        # Recherche dans la base de données Cloud
        cloud_response = self.search_database(user_message)
        if cloud_response:
            return cloud_response

        # Générer une réponse avec le modèle CTRL
        input_ids = self.tokenizer.encode(user_message, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=50, num_beams=5, early_stopping=True)
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text

    def send_message(self):
        user_message = self.user_input.get()
        self.chat_history.insert(tk.END, f"You: {user_message}\n")
        self.user_input.delete(0, tk.END)

        # Générer une réponse
        response = self.generate_response(user_message)
        self.chat_history.insert(tk.END, f"AI: {response}\n")

root = tk.Tk()
app = ChatApp(root)
root.mainloop()
