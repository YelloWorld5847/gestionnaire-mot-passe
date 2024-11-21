import customtkinter as ctk
import tkinter as tk
import random

# Couleurs
fg_color_button = "#931cff"
hover_color_button = "#6b00b3"


class PasswordApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        global frame

        self.LETTER = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.SYMBOLE = r"!@#$%^&*()_+-=[]{}|;:'\",.<>?/`~\\"
        self.NUMBER = "0123456789"

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
        # self.password_entry.insert("1.0", "r2f477e5d4")  # exemple de mot de passe généré
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
        self.slider_label = ctk.CTkLabel(frame, text="12 character", font=("Arial", 14, "bold"), text_color="#cfcfcf")
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
        self.symbol_switch_label = ctk.CTkLabel(frame, text="symbol", font=("Arial", 14, "bold"), text_color="#cfcfcf")
        self.symbol_switch_label.place(x=50, y=300)
        self.symbol_switch = ctk.CTkSwitch(frame, text="", progress_color=fg_color_button, border_color=fg_color_button,
                                           switch_height=20, switch_width=39,
                                           command=lambda: self.changeSwitch(self.symbol_switch))
        self.symbol_switch.select()
        self.symbol_switch.place(x=313, y=300)

        self.number_switch_label = ctk.CTkLabel(frame, text="number", font=("Arial", 14, "bold"), text_color="#cfcfcf")
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
                                                hover_color=hover_color_button, command=self.save)
        self.place_order_button.place(x=100, y=425)

        self.bind("<Key>", self.clavier)


        self.regenerate_password()

    def save(self):
        self.name = self.title_label.get()
        self.password = self.password_entry.get("0.0", "end")
        print(f"mot de passe enregistrer :\nnom : {self.name}\nmot de passe : {self.password}")


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

    def go_back(self):
        """Revenir à l'écran précédent"""
        print("Revenir à l'écran précédent")

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


# Ouvrir le fichier avec l'encodage UTF-8
with open('dict_fr.txt', 'r', encoding='utf-8') as file:
    mots = file.readlines()

# Supprimer les sauts de ligne et filtrer les mots de moins de 8 caractères
mots = [mot.strip() for mot in mots if len(mot.strip()) < 4]

# Vérifier qu'il y a des mots dans la liste
if mots:
    # Sélectionner un mot aléatoire
    mot_aleatoire = random.choice(mots)
    print("Mot aléatoire (moins de 8 caractères) :", mot_aleatoire)
else:
    print("Aucun mot ne correspond à la condition.")
# dzqdq
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = PasswordApp()
    app.mainloop()
