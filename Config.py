# Paramètres généraux
para_generaux= {
  'app_name': 'Hypnose_Data Manager',
  'version': '1.0',
  'auteur': 'Soro W. Lassina'
  }

# Configurer le serveur SMTP pour Gmail
para_smtp= {
  'smtp_server' : 'smtp.gmail.com',
  'smtp_port' : '587',  
  'sender_email' : 'sorolassina58@gmail.com',
  'sender_password' : "mxcu kxhv jwym staa"
}

# Paramètres de connexion à la base de données
database_local= {'host': 'mongodb://localhost:',
  'port': '27017',
  'username': 'user',
  'password': '',
  'db_Users_name': 'Hypnose_manager',
  'db_users_table': 'Manage_Users',
  'db_valide_name': 'Hypnose_documents_validés',
  'db_attente_name': 'Hypnose_documents_en_attente'
  }

database_cloud={'host_prefix' : 'mongodb+srv://',
  'username' : 'sorolassina',
  'password' : '2311SLSS@',
  'host_suffix' : '@hypnosecluster.5vtl4ex.mongodb.net/',
  'db_Users_name' : 'Hypnose_manager',
  'db_valide_name': 'Hypnose_documents_validés',
  'db_attente_name': 'Hypnose_documents_en_attente'
  }

# Image background 
images={'icone_application' : "./icones/logo2.ico",
  'icone_login' : "./icones/logo2.ico",
  'background_createlog' : "./images/logo2.png"
  }

