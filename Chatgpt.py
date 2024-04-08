import tkinter as tk
from tkinter import scrolledtext
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import pymongo

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Génération de Texte")

        # Connexion à MongoDB Cloud
        self.client_cloud = pymongo.MongoClient("mongodb+srv://sorolassina:2311SLSS@hypnosecluster.5vtl4ex.mongodb.net/")
        self.db_cloud = self.client_cloud["Hypnose_Cloud"]

        # Chargement du modèle GPT-2
        self.tokenizer = GPT2Tokenizer.from_pretrained("antoiloui/gpt2-french")
        self.model = GPT2LMHeadModel.from_pretrained("antoiloui/gpt2-french")

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
        # Créer un index de texte sur le champ "Contenu"
        self.db_cloud["Docs validés"].create_index([("Contenu", "text")])

        # Rechercher dans la collection "Docs validés" en utilisant l'opérateur $text
        cloud_result = self.db_cloud["Docs validés"].find_one({"$text": {"$search": user_message}})
        
        # Si un résultat est trouvé, retourner le contenu du résultat
        if cloud_result:
            return cloud_result["Contenu"]
    
        # Sinon, retourner None
        return None

    def generate_response(self, user_message):
        # Rechercher dans la base de données Cloud
        cloud_response = self.search_database(user_message)
        if cloud_response:
            return cloud_response
        else:
            # Générer une réponse avec GPT-2
            input_ids = self.tokenizer.encode(user_message, return_tensors="pt")
            output = self.model.generate(input_ids, max_length=50, num_return_sequences=1, pad_token_id=self.tokenizer.eos_token_id)
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
