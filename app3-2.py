import random
import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
from tkinter import messagebox
import bcrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os

# Couleurs
fg_color_button = "#931cff"
hover_color_button = "#6b00b3"
label_color = "#cfcfcf"

# Connexion à la base de données SQLite
conn = sqlite3.connect('transaction.db')
cursor = conn.cursor()

# Création de la table des utilisateurs
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT,
   password TEXT,
   salt BLOB NOT NULL
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
        login_button = ctk.CTkButton(master=frame, width=220, text="Login", command=self.gestionCompte,
                                     corner_radius=6, fg_color=fg_color_button, hover_color=hover_color_button)
        login_button.place(x=50, y=240)

    def gestionCompte(self):
        username = self.entry1.get()
        password = self.entry2.get()

        # Vérifier que les champs ne sont pas vides
        if not username or not password:
            CTkMessagebox(
                self,
                title="Erreur",
                message="Veuillez saisir un nom d'utilisateur et un mot de passe.",
                option_1="Ok",
                button_color=fg_color_button,
                button_hover_color=hover_color_button,
                icon="warning",
                sound=True
            ).get()
            return

        # Vérifier si la création de compte est activée
        if self.create_account_var.get():
            self.crer_compte(username, password)
        else:
            self.connecter_compte(username, password)

    def crer_compte(self, username, password):
        # Vérifier si le nom d'utilisateur existe déjà
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            CTkMessagebox(
                self,
                title="Erreur",
                message="Le nom d'utilisateur existe déjà.",
                option_1="Ok",
                button_color=fg_color_button,
                button_hover_color=hover_color_button,
                icon="warning",
                sound=True
            ).get()
        else:
            salt = os.urandom(16)
            # Hacher le mot de passe avant de l'enregistrer
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)',
                           (username, hashed_password, salt))
            conn.commit()

            # Récupérer le mot de passe haché pour l'utilisateur
            cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()[0]
            print(result)

            CTkMessagebox(
                self,
                title="Succès",
                message=f"Utilisateur '{username}' enregistré avec succès.",
                option_1="Ok",
                button_color=fg_color_button,
                button_hover_color=hover_color_button,
                icon="info",
                sound=True
            ).get()
            self.open_main_app(password, result, salt)
        # if user:
        #     messagebox.showerror("Erreur", "Le nom d'utilisateur existe déjà.")
        # else:
        #     salt = os.urandom(16)
        #     # Hacher le mot de passe avant de l'enregistrer
        #     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        #     cursor.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', (username, hashed_password, salt))
        #     conn.commit()
        #
        #     # Récupérer le mot de passe haché pour l'utilisateur
        #     cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
        #     result = cursor.fetchone()[0]
        #     print(result)
        #
        #     messagebox.showinfo("Succès", f"Utilisateur '{username}' enregistré avec succès.")



    def connecter_compte(self, username, password):
        # Récupérer le mot de passe haché pour l'utilisateur
        cursor.execute('SELECT user_id, password, salt FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        # Dans la méthode connecter_compte
        if result:
            # Comparer le mot de passe saisi avec le mot de passe haché dans la base de données
            stored_hashed_password = result[1]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                self.open_main_app(password, result[0], result[2])  # Connexion réussie
            else:
                CTkMessagebox(
                    self,
                    title="Erreur",
                    message="Nom d'utilisateur ou mot de passe incorrect.",
                    option_1="Ok",
                    button_color=fg_color_button,
                    button_hover_color=hover_color_button,
                    icon="warning",
                    sound=True
                ).get()
        else:
            CTkMessagebox(
                self,
                title="Erreur",
                message="Nom d'utilisateur ou mot de passe incorrect.",
                option_1="Ok",
                button_color=fg_color_button,
                button_hover_color=hover_color_button,
                icon="warning",
                sound=True
            ).get()
        # if result:
        #     # Comparer le mot de passe saisi avec le mot de passe haché dans la base de données
        #     stored_hashed_password = result[1]
        #     if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        #         self.open_main_app(password, result[0], result[2])  # Connexion réussie
        #     else:
        #         messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        # else:
        #     messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def open_main_app(self, password, user_id, salt):
        # Assure la fermeture propre de la fenêtre principale
        self.destroy()
        app = MainApp(user_id, password, salt)
        app.mainloop()



# Classe principale
class MainApp(ctk.CTk):
    def __init__(self, user_id, user_password, salt):
        super().__init__()

        self.geometry("900x500")
        self.title("Main Application")

        self.user_id = user_id
        self.user_password = user_password
        self.salt = salt
        self.key = self.generate_key_from_password(self.user_password, self.salt)

        # Création d'un cadre pour centrer les éléments
        self.header_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=0)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        # Barre de recherche
        self.search_bar = ctk.CTkEntry(self.header_frame, placeholder_text="Search...", width=470, height=40,
                                       corner_radius=10)
        self.search_bar.pack(side=tk.LEFT, padx=25, pady=25, expand=True)
        self.search_bar.bind("<KeyRelease>", self.search)

        # Bouton '+'
        self.add_button = ctk.CTkButton(self.header_frame, text="+", font=("Arial", 22),
                                        width=40, height=40, command=self.creat_pass, corner_radius=12,
                                        fg_color=fg_color_button, hover_color=hover_color_button)
        self.add_button.pack(side=tk.RIGHT, padx=25, pady=25, expand=False)

        self.body_frame = ctk.CTkFrame(self, width=1500, fg_color="transparent")
        self.body_frame.pack(side='top', fill="y", expand=True)

        # Désactiver la propagation de la taille pour body_frame
        self.body_frame.pack_propagate(False)


        self.update = False
        all_passwords = self.get_all_passwords()
        self.show_passwords(all_passwords)

        # Initialisez votre interface ici
        # self.password_app = PasswordApp(self)


    def generate_key_from_password(self, password, salt):
        """Génère une clé de chiffrement à partir du mot de passe de l'utilisateur."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_data(self, data):
        """Chiffre les données avec la clé dérivée."""
        fernet = Fernet(self.key)
        return fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        """Déchiffre les données avec la clé dérivée."""
        fernet = Fernet(self.key)
        return fernet.decrypt(encrypted_data).decode()

    def search(self, event):
        search_value = self.search_bar.get()
        print(f"search = {search_value}")
        if not search_value:
            if not self.update:
                results = self.get_all_passwords()
                print(f"result in search : {results}")
                self.update = True
            else:
                return
        else:
            # # Requête SQL avec paramètres pour chercher dans les deux colonnes
            # cursor.execute('''
            #     SELECT password_id, service_name, password FROM passwords
            #     WHERE LOWER(service_name) LIKE LOWER(?) OR LOWER(password) LIKE LOWER(?)
            # ''', ('%' + search_value + '%', '%' + search_value + '%'))
            #
            # # Récupérer les résultats
            # results = cursor.fetchall()
            # decrypted_passwords = [
            #     (password_id, self.decrypt_data(service_name), self.decrypt_data(password))
            #     for password_id, service_name, password in results
            # ]

            decrypted_passwords = self.get_all_passwords()

            # Effectuer une recherche insensible à la casse
            search_value_lower = search_value.lower()
            results = [
                (password_id, service_name, password)
                for password_id, service_name, password in decrypted_passwords
                if search_value_lower in service_name.lower() or search_value_lower in password.lower()
            ]

            self.update = False
        self.show_passwords(results)

    def creat_pass(self):
        # Créer une nouvelle fenêtre pour créer un mot de passe
        password_window = PasswordApp(self)
        password_window.mainloop()  # Verrouille la fenêtre principale jusqu'à la fermeture de la fenêtre secondaire

    def update_credentials(self, name, password):
        # Mettez à jour les attributs avec les valeurs fournies par PasswordApp
        self.saved_name = name
        self.saved_password = password
        self.add_password(self.saved_name, self.saved_password)
        print(f"Nom enregistré : {self.saved_name}\nMot de passe enregistré : {self.saved_password}")

    def add_password(self, service_name, password):
        """Chiffre le service et le mot de passe avant de les enregistrer dans la base."""
        encrypted_service = self.encrypt_data(service_name)
        encrypted_password = self.encrypt_data(password)
        cursor.execute(
            "INSERT INTO passwords (user_id, service_name, password) VALUES (?, ?, ?)",
            (self.user_id, encrypted_service, encrypted_password)
        )
        conn.commit()
        all_passwords = self.get_all_passwords()
        self.show_passwords(all_passwords)

    def update_password(self, password_id, new_service_name, new_password):
        # Mettre à jour le mot de passe et le nom du service dans la base de données
        cursor.execute('''
        UPDATE passwords
        SET service_name = ?, password = ?
        WHERE password_id = ?
        ''', (new_service_name, new_password, password_id))
        conn.commit()

        # Vérifie si une ligne a été modifiée
        if cursor.rowcount > 0:
            print("Mot de passe mis à jour avec succès.")
            all_passwords = self.get_all_passwords()
            self.show_passwords(all_passwords)
        else:
            print("Aucun mot de passe trouvé avec cet ID.")

    def get_all_passwords(self):
        """Récupère et déchiffre tous les mots de passe de l'utilisateur."""
        cursor.execute("SELECT password_id, service_name, password FROM passwords WHERE user_id = ?", (self.user_id,))
        encrypted_passwords = cursor.fetchall()
        print(encrypted_passwords)
        decrypted_passwords = [
            (password_id, self.decrypt_data(service_name), self.decrypt_data(password))
            for password_id, service_name, password in encrypted_passwords
        ]
        print(decrypted_passwords)
        self.update = True
        return decrypted_passwords

    def get_password(self, password_id):
        cursor.execute("SELECT service_name, password FROM passwords WHERE password_id = ?", (password_id,))
        return cursor.fetchall()

    def cut_text(self, text, max_char):
        if len(text) > max_char:
            return text[:max_char] + "..."
        else:
            return text

    def split_text_with_gradient(self, text, max_char):
        """Divise le texte et ajoute une couleur de plus en plus grise aux derniers caractères."""
        if len(text) > max_char:
            visible_part = text[:max_char - 6]  # Garder les premiers caractères visibles sans effet
            fade_part = text[max_char - 5:max_char]  # Derniers caractères pour le dégradé
            colors = [label_color, "gray80", "gray60", "gray40", "gray30", "gray20"]
            # Associe chaque caractère de fade_part avec une couleur dégradée
            return [(visible_part, label_color)] + [(char, colors[i]) for i, char in enumerate(fade_part)]
        else:
            return [(text, label_color)]

    def show_passwords(self, passwords):
        for widget in self.body_frame.winfo_children():
            widget.destroy()

        # passwords = self.get_all_passwords(self.user_id)

        # Fonction appelée lors du clic sur un mot de passe
        def on_click(event, password_id):
            print(f"clique sur la frame : {password_id}")
            passwords2 = self.get_password(password_id)
            print(passwords2)
            password_window = PasswordApp(self, password_id, passwords2[0][0], passwords2[0][1])
            password_window.mainloop()  # Verrouille la fenêtre principale jusqu'à la fermeture de la fenêtre secondaire


        # Nombre de colonnes maximum par ligne
        max_columns = 2
        row = 0
        column = 0

        # Créer un frame pour chaque mot de passe
        for password_id, service_name, password in passwords:
            service_name = str(service_name).replace('\n', '')
            password = str(password).replace('\n', '')
            frame = ctk.CTkFrame(self.body_frame, border_width=4, corner_radius=14, width=350, height=75)
            frame.grid(row=row, column=column, padx=20, pady=20, sticky="nw")  # sticky="nw" pour aligner en haut à gauche
            frame.pack_propagate(False)

            # Lier l'événement de clic à la frame
            frame.bind("<Button-1>", lambda event, pid=password_id: on_click(event, pid))

            # def bind_clicks_to_frame(frame, password_id):
            #     frame.bind("<Button-1>", lambda event: on_click(event, password_id))
            #     for child in frame.winfo_children():
            #         child.bind("<Button-1>", lambda event, pid=password_id: on_click(event, pid))
            #
            # bind_clicks_to_frame(frame, password_id)

            # Créer un frame pour le nom du service
            service_frame = ctk.CTkFrame(frame, fg_color="transparent")
            service_frame.pack(side="top", fill="x", pady=(10, 0), padx=30)
            service_frame.bind("<Button-1>", lambda event, pid=password_id: on_click(event, pid))
            # Diviser et styliser le nom du service avec un dégradé
            service_name_parts = self.split_text_with_gradient(service_name, 31)
            for i, (part, color) in enumerate(service_name_parts):
                service_label = ctk.CTkLabel(service_frame, text=part, font=("Courier", 16, "bold"), anchor="w",
                                             text_color=color)
                service_label.pack(side="left")
                service_label.bind("<Button-1>", lambda event, pid=password_id: on_click(event, pid))

            # Créer un frame pour le mot de passe
            password_frame = ctk.CTkFrame(frame, fg_color="transparent")
            password_frame.pack(side="top", fill="x", pady=(5, 7), padx=30)
            password_frame.bind("<Button-1>", lambda event, pid=password_id: on_click(event, pid))
            # Diviser et styliser le mot de passe avec un dégradé
            password_parts = self.split_text_with_gradient(password, 34)
            for i, (part, color) in enumerate(password_parts):
                password_label = ctk.CTkLabel(password_frame, text=part, font=("Courier", 14), anchor="w",
                                              text_color=color)
                password_label.pack(side="left")
                password_label.bind("<Button-1>", lambda event, pid=password_id: on_click(event, pid))

            # Gérer la disposition en colonnes et lignes
            column += 1
            if column >= max_columns:
                column = 0
                row += 1


class PasswordApp(ctk.CTk):
    def __init__(self, main_app, password_id=None, name_password="", password=""):
        super().__init__()
        global frame


        self.LETTER = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.SYMBOLE = r"!@#$%^&*()_+-=[]{}|;:'\",.<>?/`~\\"
        self.NUMBER = "0123456789"

        self.main_app = main_app  # Conservez une référence à MainApp
        self.password_id = password_id

        self.geometry("400x500")
        self.title("Password Manager")

        # Interface graphique pour la fenêtre de connexion
        frame = ctk.CTkFrame(master=self, corner_radius=15, width=400, height=500)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Titre "Password Name"
        self.title_label = ctk.CTkEntry(frame, font=("Arial", 20, "bold"),
                                        placeholder_text="Password Name",
                                        border_width=0,
                                        fg_color="transparent",
                                        width=300,
                                        justify="center")
        if name_password != "":
            self.title_label.insert(0, name_password)
        self.title_label.place(relx=0.52, y=30, anchor=tk.CENTER)

        # Bouton '<' pour revenir
        self.back_button = ctk.CTkButton(frame, text="\u2B9C", width=40, height=40,
                                         command=self.go_back,
                                         text_color="white",
                                         font=("Arial", 20, "bold"),
                                         fg_color="transparent",
                                         hover_color="#931cff",
                                         corner_radius=10)
        self.back_button.place(x=10, y=10)

        # Ajouter un séparateur
        self.add_separator(60)

        # Barre de mot de passe avec le bouton de régénération
        self.password_entry = ctk.CTkTextbox(frame, width=260, height=57, font=("Courier", 16),
                                           border_width=3, fg_color='#343638')  # justify="center"
        self.password_entry.insert("1.0", password)  # exemple de mot de passe généré
        self.password_entry.place(relx=0.44, y=110, anchor=ctk.CENTER)

        self.regen_button = ctk.CTkButton(frame, text="↻", width=37, height=37, command=self.regenerate_password,
                                          fg_color=fg_color_button, font=("Arial", 20, "bold"),
                                          hover_color=hover_color_button)  # fg_color="#343638", hover_color='#2F2F30'
        self.regen_button.place(x=333, y=110, anchor=ctk.CENTER)

        self.pass_type_frame = ctk.CTkFrame(frame, width=310, height=34, corner_radius=10, fg_color="transparent")
        self.pass_type_frame.place(relx=0.5, y=170, anchor=ctk.CENTER)

        # Boutons pour les types de mot de passe
        self.random_button = ctk.CTkButton(self.pass_type_frame, text="random", width=100, height=33,
                                           fg_color=fg_color_button, hover_color=hover_color_button,
                                           font=("Arial", 14, "bold"),
                                           command=lambda: self.select_button(self.random_button))
        self.random_button.place(relx=0.16, rely=0.5, anchor=ctk.CENTER)

        self.memorable_button = ctk.CTkButton(self.pass_type_frame, text="memorable", width=100, height=33,
                                              fg_color="#7e7e7e", hover_color=hover_color_button,
                                              font=("Arial", 14, "bold"),
                                              command=lambda: self.select_button(self.memorable_button))
        self.memorable_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.pin_button = ctk.CTkButton(self.pass_type_frame, text="PIN code", width=100, height=33,
                                        fg_color="#7e7e7e", hover_color=hover_color_button,
                                        font=("Arial", 14, "bold"),
                                        command=lambda: self.select_button(self.pin_button))
        self.pin_button.place(relx=0.84, rely=0.5, anchor=ctk.CENTER)

        self.randomVar = 12
        self.memorableVar = 3
        self.pinCodeVar = 3


        # Sélectionner le bouton par défaut
        self.select_button(self.random_button)

        # Ajouter un séparateur
        self.add_separator(210)

        # Slider pour la longueur du mot de passe
        self.slider_label = ctk.CTkLabel(frame, text="12 character", font=("Arial", 14, "bold"), text_color=label_color)
        self.slider_label.place(x=50, y=230)

        self.length_slider_var = ""
        self.length_slider = ctk.CTkSlider(frame, from_=8, to=26, number_of_steps=18, command=self.update_slider_label,
                                           width=200, button_color="white", border_width=3, height=20, progress_color=fg_color_button,
                                           button_hover_color='dark gray')
        self.length_slider.set(self.randomVar)  # Définir la valeur initiale sur 12
        self.length_slider.place(x=158, y=237)

        # Ajouter un séparateur
        self.add_separator(280)

        # Boutons switch pour 'symbol' et 'number'
        self.symbol_switch_label = ctk.CTkLabel(frame, text="symbol", font=("Arial", 14, "bold"), text_color=label_color)
        self.symbol_switch_label.place(x=50, y=300)
        self.symbol_switch = ctk.CTkSwitch(frame, text="", progress_color=fg_color_button, border_color=fg_color_button,
                                           switch_height=20, switch_width=39,
                                           command=lambda: self.changeSwitch(self.symbol_switch))
        self.symbol_switch.select()
        self.symbol_switch.place(x=313, y=300)

        self.number_switch_label = ctk.CTkLabel(frame, text="number", font=("Arial", 14, "bold"), text_color=label_color)
        self.number_switch_label.place(x=50, y=345)
        self.number_switch = ctk.CTkSwitch(frame, text="", progress_color=fg_color_button, border_color=fg_color_button,
                                           switch_height=20, switch_width=39,
                                           command=lambda: self.changeSwitch(self.number_switch))
        self.number_switch.select()
        self.number_switch.place(x=313, y=345)

        # Ajouter un séparateur
        self.add_separator(390)

        # Bouton 'Save'
        self.place_order_button = ctk.CTkButton(frame, text="Save", fg_color="#931cff", width=200, height=40,
                                                text_color=label_color, hover_color=hover_color_button, command=self.save)
        self.place_order_button.place(x=100, y=425)

        self.bind("<Key>", self.clavier)

        if password == "":
            self.regenerate_password()

    def save(self):
        self.name = self.title_label.get().strip()
        self.password = self.password_entry.get("0.0", "end").strip()

        if self.password_id == None:
            # Appelez la méthode update_credentials de MainApp pour enregistrer les valeurs
            self.main_app.add_password(self.name, self.password)
        else:
            self.main_app.update_password(self.password_id, self.name, self.password)
        print(f"Mot de passe enregistré :\nNom : {self.name}\nMot de passe : {self.password}")
        self.destroy()


    def go_back(self):
            """Revenir à l'écran précédent"""
            if self.confirm_return():
                self.destroy()

    def confirm_return(self):
        # Affiche la boîte de message de confirmation
        response = CTkMessagebox(
            self,
            title="Confirmation",
            message="Êtes-vous sûr de vouloir revenir sans enregistrer ?",
            option_1="Oui",
            option_2="Annuler",
            button_color=fg_color_button,
            button_hover_color=hover_color_button,
            icon="warning",
            sound=True,
            option_focus=2
        ).get()

        # Vérifie la réponse de l'utilisateur
        if response == "Oui":
            print("Retour sans sauvegarder")  # Remplace par l'action de retour sans sauvegarde
            return True
        else:
            print("Annulation du retour")  # Reste sur la page actuelle
            return False


    def changeSwitch(self, switch):
        if switch.get():
            switch.configure(border_color=fg_color_button)
        else:
            switch.configure(border_color='gray')

    def select_word(self):
        # Ouvrir le fichier et lire les mots
        with open('dict_fr.txt', 'r', encoding='utf-8') as file:
            mots = file.readlines()

        # Supprimer les éventuels sauts de ligne ou espaces
        mots = [mot.strip() for mot in mots]

        # Sélectionner un mot aléatoire
        mot_aleatoire = random.choice(mots)

        return mot_aleatoire

    def creat_pass(self, num_char, symbol, number):
        if self.buton_selectione == "memorable":
            pass_word = ""
            for char in range(int(num_char)):
                pass_word += self.select_word()
                if char != num_char - 1:
                    pass_word += "-"

            return pass_word

        elif self.buton_selectione == "random":
            CHARACTERE = self.LETTER
            if symbol == 1:
                CHARACTERE += self.SYMBOLE
            if number == 1:
                CHARACTERE += self.NUMBER

        elif self.buton_selectione == "PIN code":
            CHARACTERE = self.NUMBER

        pass_word = ""
        for char in range(int(num_char)):
            pass_word += random.choice(CHARACTERE)

        # [random.choice(CHARACTERE) for char in range(num_char)]

        return pass_word

    def select_button(self, selected_button):
        self.buton_selectione = selected_button._text
        """Changer la couleur du bouton sélectionné et désactiver les autres"""
        buttons = [self.random_button, self.memorable_button, self.pin_button]
        for button in buttons:
            button.configure(fg_color="#626262", state="normal")

        # Appliquer la couleur de sélection au bouton choisi
        selected_button.configure(fg_color=fg_color_button, text_color="white")

        # if selected_button.winfo_name() == "!ctkbutton2":
        self.update_slider_range()

    def clavier(self, event):
        caractere = event.char
        # print(caractere)
        if caractere == "1":
            print("le caractère est 1")
            self.pass_type_frame.lift()
        elif caractere == "2":
            print("le caractère est 2")
        elif caractere == "3":
            print("le caractère est 3")

    def add_separator(self, y_pos):
        """Ajouter un séparateur à la position y donnée"""
        separator = ctk.CTkFrame(frame, height=2, fg_color="gray", width=360)
        separator.place(x=20, y=y_pos)

    def regenerate_password(self):
        sybol_T_F = self.symbol_switch.get()
        number_T_F = self.number_switch.get()
        len_passord = self.length_slider.get()
        self.password = self.creat_pass(len_passord, sybol_T_F, number_T_F)
        self.password_entry.delete("1.0", tk.END)
        self.password_entry.insert("1.0", self.password)

    def update_slider_label(self, value):
        print(f"valeur : {value}")
        """Mettre à jour le label du slider"""
        if self.buton_selectione == "memorable":
            self.memorableVar = value
            print(self.memorableVar)
        elif self.buton_selectione == "PIN code":
            self.pinCodeVar = value
            print(self.pinCodeVar)
        else:
            self.randomVar = value
            print(self.randomVar)



        self.slider_label.configure(text=f"{int(value)} character")
        self.regenerate_password()

    def update_slider_range(self):
        # Récupérer la valeur actuelle et le pourcentage par rapport à la plage actuelle
        # current_value = self.length_slider.get()
        # old_min = 4
        # old_max = 20
        # relative_position = (current_value - old_min) / (old_max - old_min)
        #
        # # Nouvelle plage de 3 à 6
        # new_min = 3
        # new_max = 6
        #
        # # Calculer la nouvelle valeur en maintenant le même pourcentage de position
        # new_value = new_min + relative_position * (new_max - new_min)

        try:
            # Mettre à jour la plage et la valeur du slider
            if self.buton_selectione == "memorable":
                self.length_slider.configure(from_=3, to=6, number_of_steps=3)
                self.length_slider.set(self.memorableVar)  # Appliquer la nouvelle valeur
                self.update_slider_label(self.memorableVar)
            elif self.buton_selectione == "PIN code":
                self.length_slider.configure(from_=3, to=20, number_of_steps=18)
                self.length_slider.set(self.pinCodeVar)  # Appliquer la nouvelle valeur
                self.update_slider_label(self.pinCodeVar)
            else:
                self.length_slider.configure(from_=8, to=25, number_of_steps=18)
                self.length_slider.set(self.randomVar)  # Appliquer la nouvelle valeur
                self.update_slider_label(self.randomVar)
        except Exception as e:
            print("le slide n'a pas été encore créé")


# Lancer l'application
if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()

# Fermer la connexion
conn.close()
print("Fermer la connexion")