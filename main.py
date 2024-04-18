import tkinter as tk
from Loginconnect import Login

import yaml

# Charger le fichier de configuration YAML
with open('Config.yaml', 'r') as fichier_config:
    config = yaml.safe_load(fichier_config)

# Maintenant, vous pouvez utiliser les paramètres de configuration dans votre application
nom_application = config['app_name']
version = config['version']
auteur = config['auteur']
auteur = config['auteur']




if __name__ == "__main__":  
    root = tk.Tk()
    app = Login(root)  # Passer le widget parent (root) comme argument
    root.mainloop()