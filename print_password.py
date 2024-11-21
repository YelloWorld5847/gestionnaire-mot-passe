import sqlite3
from hashlib import sha256

# Connexion à la base de données (ou création)
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

# Création des tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS passwords (
    password_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    service_name TEXT NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
''')
conn.commit()

# Fonction pour hacher le mot de passe
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Enregistrement d'un nouvel utilisateur
def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, hash_password(password)))
        conn.commit()
        print("Utilisateur enregistré avec succès.")
    except sqlite3.IntegrityError:
        print("Le nom d'utilisateur est déjà pris.")

# Authentification d'un utilisateur
def authenticate_user(username, password):
    cursor.execute("SELECT user_id, password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and result[1] == hash_password(password):
        print("Connexion réussie.")
        return result[0]  # Retourne l'ID de l'utilisateur
    else:
        print("Nom d'utilisateur ou mot de passe incorrect.")
        return None

# Enregistrement d'un mot de passe pour un utilisateur
def add_password(user_id, service_name, password):
    cursor.execute("INSERT INTO passwords (user_id, service_name, password) VALUES (?, ?, ?)",
                   (user_id, service_name, password))
    conn.commit()
    print("Mot de passe ajouté avec succès.")


# # Exemple d'utilisation
# register_user("testuser", "monmotdepasse")
# user_id = authenticate_user("testuser", "monmotdepasse")
#
# if user_id:
#     add_password(user_id, "Gmail", "motdepassegmail123")
#     add_password(user_id, "Facebook", "motdepassefacebook456")

import tkinter as tk
from tkinter import messagebox

# Exemple de connexion (dans un contexte réel, tu récupèrerais user_id depuis l'authentification)
user_id = authenticate_user("testuser", "monmotdepasse")  # Supposons que user_id est valide

def get_passwords(user_id):
    cursor.execute("SELECT password_id, service_name, password FROM passwords WHERE user_id = ?", (user_id,))
    return cursor.fetchall()


# Fonction pour créer l'interface graphique et afficher les mots de passe
def show_passwords(user_id):
    passwords = get_passwords(user_id)

    # Fenêtre principale Tkinter
    root = tk.Tk()
    root.title("Gestion des mots de passe")

    # Fonction appelée lors du clic sur un mot de passe
    def on_click(event, password_id):
        print(f"ID du mot de passe : {password_id}")

    # Créer un frame pour chaque mot de passe
    for password_id, service_name, password in passwords:
        frame = tk.Frame(root, borderwidth=2, relief="solid", padx=10, pady=5)
        frame.pack(pady=5, fill="x")

        # Lier l'événement de clic à la frame
        frame.bind("<Button-1>", lambda event, pid=password_id: on_click(event, pid))

        # Ajout du texte pour chaque mot de passe
        service_label = tk.Label(frame, text=f"Service : {service_name}")
        service_label.pack(side="left")

        password_label = tk.Label(frame, text=f"Mot de passe : {password}")
        password_label.pack(side="left", padx=10)

        # # Ajouter un bouton qui, lorsqu'il est cliqué, affiche l'ID du mot de passe
        # btn = tk.Button(frame, text="Afficher ID", command=lambda pid=password_id: on_click(pid))
        # btn.pack(side="right")

    # Lancer l'interface Tkinter
    root.mainloop()


# Afficher les mots de passe pour l'utilisateur connecté
if user_id:
    show_passwords(user_id)
else:
    print("Utilisateur non authentifié.")
