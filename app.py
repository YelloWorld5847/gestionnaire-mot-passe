import tkinter as tk
import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import bcrypt

# Couleurs
fg_color_button = "#931cff"
hover_color_button = "#6b00b3"

# Connexion à la base de données SQLite
conn = sqlite3.connect('transaction.db')
cursor = conn.cursor()

# Création de la table des utilisateurs
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT,
   password TEXT
)
''')

# Configurer l'apparence de customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


# Classe pour la fenêtre principale de connexion
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x440")
        self.title('Login')

        # Interface graphique pour la fenêtre de connexion
        frame = ctk.CTkFrame(master=self, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        l2 = ctk.CTkLabel(master=frame, text="Log into your Account", font=('Century Gothic', 20))
        l2.place(x=50, y=45)

        self.entry1 = ctk.CTkEntry(master=frame, width=220, placeholder_text='Username')
        self.entry1.place(x=50, y=110)

        self.entry2 = ctk.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*●")
        self.entry2.place(x=50, y=165)

        # Case à cocher pour activer/désactiver la création de compte
        self.create_account_var = tk.BooleanVar()
        create_account_checkbox = ctk.CTkCheckBox(master=frame, text="Create an account",
                                                  variable=self.create_account_var, fg_color=fg_color_button,
                                                  hover_color=hover_color_button)
        create_account_checkbox.place(x=50, y=300)

        # Bouton de connexion
        login_button = ctk.CTkButton(master=frame, width=220, text="Login", command=self.enregistrer_utilisateur,
                                     corner_radius=6, fg_color=fg_color_button, hover_color=hover_color_button)
        login_button.place(x=50, y=240)

    def enregistrer_utilisateur(self):
        username = self.entry1.get()
        password = self.entry2.get()

        # Vérifier que les champs ne sont pas vides
        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez saisir un nom d'utilisateur et un mot de passe.")
            return

        # Vérifier si la création de compte est activée
        if self.create_account_var.get():
            # Vérifier si le nom d'utilisateur existe déjà
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                messagebox.showerror("Erreur", "Le nom d'utilisateur existe déjà.")
            else:
                # Hacher le mot de passe avant de l'enregistrer
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
                conn.commit()
                messagebox.showinfo("Succès", f"Utilisateur '{username}' enregistré avec succès.")
                self.open_main_app()
        else:
            # Récupérer le mot de passe haché pour l'utilisateur
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user:
                # Comparer le mot de passe saisi avec le mot de passe haché dans la base de données
                stored_hashed_password = user[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                    self.open_main_app()  # Connexion réussie
                else:
                    messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
            else:
                messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def open_main_app(self, user_id=None):
        # Assure la fermeture propre de la fenêtre principale
        self.destroy()
        app = MainApp()
        app.mainloop()


# Classe pour la nouvelle fenêtre après connexion
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x400")
        self.title("Main Application")

        # Création d'un cadre pour centrer les éléments
        self.top_fram = ctk.CTkFrame(self, fg_color="transparent")
        self.top_fram.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)

        # Barre de recherche
        self.search_bar = ctk.CTkEntry(self.top_fram, placeholder_text="Search...", width=400)
        self.search_bar.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

        # Bouton '+'
        self.add_button = ctk.CTkButton(self.top_fram, text="+", width=50, command=self.add_pass,
                                        fg_color=fg_color_button, hover_color=hover_color_button)
        self.add_button.pack(side=tk.RIGHT, padx=5, pady=5, expand=False)

    def add_pass(self):
        # Masquer la première frame
        self.top_fram.pack_forget()

        # Créer une nouvelle frame prenant toute la fenêtre
        self.pass_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pass_frame.pack(fill=tk.BOTH, expand=True)

        self.add_separator()

        # Bouton '<' pour revenir en arrière
        self.back_button = ctk.CTkButton(self.pass_frame, text="<", width=40, height=40,
                                         command=self.go_back,
                                         text_color="#F1F1F1",
                                         font=("Arial", 20, "bold"),
                                         fg_color="transparent",
                                         hover_color=fg_color_button,  # Violet au survol
                                         corner_radius=10)
        self.back_button.place(x=20, y=20)

        # Entry pour le nom du mot passe
        self.pass_name = ctk.CTkEntry(self.pass_frame, width=220, placeholder_text='Password name',
                                      fg_color="transparent", border_width=0)
        self.pass_name.place(x=50, y=20)

        self.add_separator()

    def go_back(self):
        # Revenir à l'écran principal
        self.pass_frame.pack_forget()  # Masquer la nouvelle frame
        self.top_fram.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)  # Afficher la première frame

    def add_separator(self):
        """Fonction pour ajouter un séparateur"""
        separator = ctk.CTkFrame(self.pass_frame, height=2, fg_color="gray")
        separator.pack(fill="x", padx=15, pady=10)


# Lancer l'application
if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()

# Fermer la connexion
conn.close()

