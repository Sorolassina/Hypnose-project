#from pickle import NONE
import tkinter as tk
import webbrowser
from PIL import Image, ImageTk
from tkinter import filedialog

import sys
sys.path.append("C:/Hypnose_Python/controllers")

# Assurez-vous d'importer correctement vos contrôleurs
from controllers.upload_controller import upload_file
from controllers.read_controller import read_file
from controllers.update_controller import update_file
from controllers.delete_controller import delete_file

class Application(tk.Tk):
   
    def __init__(self, master=None):    
        self.master = master   
        self.window_width = 800
        self.window_height = 400
        self.center_window()
        self.master.resizable(False, False)
        self.master.title("Application de gestion Hypnose DataBase")
        #self.set_background() 
        self.manage_object()
        self.manage_collection()
                   
    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.master.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        
    def set_background(self):
        # Charger l'image de fond d'écran
        img = Image.open("./images/Hypnose.jpg")  # Replace "background.jpg" with your image file path
        img = img.resize((800, 400), Image.LANCZOS)  # Resize image to fit window size
        img = ImageTk.PhotoImage(img)
        # Créer un label pour le fond d'écran
        background_label = tk.Label(self.master, image=img)
        background_label.image = img  # Keep a reference to the image to prevent garbage collection
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place label in the entire window    
   
    def manage_object(self):
        # Upload Button
        self.upload_button = tk.Button(text="Upload", command=self.upload_file)   
        # Display Button
        self.display_button = tk.Button(text="Display", command=self.display_file)  
        # Update Button
        self.update_button = tk.Button(text="Update", command=self.update_file)       
        # Delete Button
        self.delete_button = tk.Button(text="Delete", command=self.delete_file)   
        #Lien vers le site internet hypnose
        self.Bouton_site=tk.Button(text="Site internet",command=self.open_site,bg="white")
        
    def manage_collection(self):
        # Collection Selection Buttons
        self.pdf_button = tk.Button(text="PDF Collection", command=lambda: self.display_collection("pdf"))
        self.pdf_button.pack(side=tk.LEFT, padx=4, pady=4)
        
        self.text_button = tk.Button(text="Text Collection", command=lambda: self.display_collection("text"))
        #self.text_button.pack(side=tk.LEFT, padx=4, pady=4)

        self.csv_button = tk.Button(text="CSV Collection", command=lambda: self.display_collection("csv"))
        #self.csv_button.pack(side=tk.LEFT, padx=4, pady=4)

#Codes déterminant les actions des boutons du formulaire
    #Redirige vers le site
    def open_site(self):
        webbrowser.open_new("https://www.hypnose-aventures.com/") # Ce bouton vous redirige vers votre site internet

    #Charge les fichiers sur la base de données Hadoop
    def upload_file(self):
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            file_type = file_path.split(".")[-1]
            if file_type in ["pdf", "txt", "csv"]:
                success = upload_file(file_path, file_type)
                if success:
                    print(f"File '{file_path}' uploaded successfully!")
                else:
                    print(f"Failed to upload file '{file_path}'.")
            else:
                print(f"Unsupported file format for file '{file_path}'.")

    def display_file(self):
        file_id = "5fbbba2ecff45b3f58ea80e4"  # Example file ID, replace with actual ID from MongoDB
        file_type = "pdf"  # Example file type, replace with actual file type
        file_content = read_file(file_id, file_type)
        if file_content:
            # Display file content using appropriate method
            print("File content:", file_content)
        else:
            print("Failed to retrieve file.")

    def update_file(self):
        file_id = "5fbbba2ecff45b3f58ea80e4"  # Example file ID, replace with actual ID from MongoDB
        file_type = "pdf"  # Example file type, replace with actual file type
        updated_content = "Updated content"  # Example updated content, replace with actual content
        success = update_file(file_id, file_type, updated_content)
        if success:
            print("File updated successfully!")
        else:
            print("Failed to update file.")

    def delete_file(self):
        file_id = "5fbbba2ecff45b3f58ea80e4"  # Example file ID, replace with actual ID from MongoDB
        file_type = "pdf"  # Example file type, replace with actual file type
        success = delete_file(file_id, file_type)
        if success:
            print("File deleted successfully!")
        else:
            print("Failed to delete file.")
               

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

