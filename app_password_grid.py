import customtkinter as ctk
import tkinter as tk
import random

from app import fg_color_button, hover_color_button
from main import CHARACTERE


class PasswordApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x500")
        self.title("Password Manager")

        # Interface graphique pour la fenêtre de connexion
        frame = ctk.CTkFrame(master=self, corner_radius=15)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre "Password Name"
        self.title_label = ctk.CTkEntry(frame, font=("Arial", 20, "bold"),
                                        placeholder_text="Password Name",
                                        border_width=0,
                                        fg_color="transparent",
                                        justify="center")
        self.title_label.grid(row=0, column=1, pady=(10, 20))

        # Bouton '<' pour revenir
        self.back_button = ctk.CTkButton(frame, text="\u2B9C", width=40, height=40,
                                         command=self.go_back,
                                         text_color="white",
                                         font=("Arial", 20, "bold"),
                                         fg_color="transparent",
                                         hover_color="#931cff",
                                         corner_radius=10)
        self.back_button.grid(row=0, column=0, padx=10, pady=(10, 0))

        # Ajouter un séparateur
        self.add_separator(frame, 1)

        # Barre de mot de passe avec le bouton de régénération
        self.password_entry = ctk.CTkEntry(frame, justify="center", font=("Arial", 16))
        self.password_entry.insert(0, "r2f477e5d4")  # exemple de mot de passe généré
        self.password_entry.grid(row=2, column=1, pady=10)

        self.regen_button = ctk.CTkButton(frame, text="↻", width=30, height=29, command=self.regenerate_password,
                                          fg_color="#343638", font=("Arial", 20, "bold"), corner_radius=0,
                                          hover_color='#2F2F30')
        self.regen_button.grid(row=2, column=2, padx=10)

        # Frame pour les types de mot de passe
        self.pass_type_frame = ctk.CTkFrame(frame, corner_radius=10, fg_color="transparent")
        self.pass_type_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # Boutons pour les types de mot de passe
        self.random_button = ctk.CTkButton(self.pass_type_frame, text="random",
                                           fg_color=fg_color_button, hover_color=hover_color_button,
                                           command=lambda: self.select_button(self.random_button))
        self.random_button.pack(side="left", padx=10)

        self.memorable_button = ctk.CTkButton(self.pass_type_frame, text="memorable",
                                              fg_color="#7e7e7e", hover_color=hover_color_button,
                                              command=lambda: self.select_button(self.memorable_button))
        self.memorable_button.pack(side="left", padx=10)

        self.pin_button = ctk.CTkButton(self.pass_type_frame, text="PIN code",
                                        fg_color="#7e7e7e", hover_color=hover_color_button,
                                        command=lambda: self.select_button(self.pin_button))
        self.pin_button.pack(side="left", padx=10)

        # Sélectionner le bouton par défaut
        self.select_button(self.random_button)

        # Ajouter un séparateur
        self.add_separator(frame, 4)

        # Slider pour la longueur du mot de passe
        self.slider_label = ctk.CTkLabel(frame, text="12 character")
        self.slider_label.grid(row=5, column=0, padx=10, pady=10)

        self.length_slider = ctk.CTkSlider(frame, from_=8, to=26, number_of_steps=18, command=self.update_slider_label,
                                           button_color=fg_color_button, button_hover_color=hover_color_button)
        self.length_slider.set(12)
        self.length_slider.grid(row=5, column=1, columnspan=2)

        # Ajouter un séparateur
        self.add_separator(frame, 6)

        # Boutons switch pour 'symbol' et 'number'
        self.symbol_switch = ctk.CTkSwitch(frame, text="symbol", progress_color=fg_color_button)
        self.symbol_switch.select()
        self.symbol_switch.grid(row=7, column=0, padx=10, pady=10)

        self.number_switch = ctk.CTkSwitch(frame, text="number", progress_color=fg_color_button)
        self.number_switch.select()
        self.number_switch.grid(row=7, column=1, padx=10, pady=10)

        # Ajouter un séparateur
        self.add_separator(frame, 8)

        # Bouton 'Place order'
        self.place_order_button = ctk.CTkButton(frame, text="Place order", fg_color="#931cff", width=200, height=40)
        self.place_order_button.grid(row=9, column=0, columnspan=3, pady=20)

        self.bind("<Key>", self.clavier)

        self.LETTER = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.SYMBOLE = r"!@#$%^&*()_+-=[]{}|;:'\",.<>?/`~\\"
        self.NUMBER = "0123456789"


    def select_word(self):
        # Ouvrir le fichier et lire les mots
        with open('dict_fr.txt', 'r', encoding='utf-8') as file:
            mots = file.readlines()

        # Supprimer les éventuels sauts de ligne ou espaces
        mots = [mot.strip() for mot in mots]

        # Sélectionner un mot aléatoire
        mot_aleatoire = random.choice(mots)
        print(mot_aleatoire)
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

        return pass_word

    def select_button(self, selected_button):
        self.buton_selectione = selected_button._text
        buttons = [self.random_button, self.memorable_button, self.pin_button]
        for button in buttons:
            button.configure(fg_color="#626262", state="normal")
        selected_button.configure(fg_color=fg_color_button, state="disabled")
        self.update_slider_range()

    def clavier(self, event):
        caractere = event.char
        if caractere == "1":
            print("le caractère est 1")
            self.pass_type_frame.lift()
        elif caractere == "2":
            print("le caractère est 2")
        elif caractere == "3":
            print("le caractère est 3")

    def add_separator(self, frame, row):
        separator = ctk.CTkFrame(frame, height=2, fg_color="gray")
        separator.grid(row=row, column=0, columnspan=3, sticky="ew", pady=10)

    def regenerate_password(self):
        sybol_T_F = self.symbol_switch.get()
        number_T_F = self.number_switch.get()
        len_passord = self.length_slider.get()
        self.password = self.creat_pass(len_passord, sybol_T_F, number_T_F)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, self.password)

    def go_back(self):
        print("Revenir à l'écran précédent")

    def update_slider_label(self, value):
        self.slider_label.configure(text=f"{int(value)} character")
        self.regenerate_password()

    def update_slider_range(self):
        try:
            if self.buton_selectione == "memorable":
                self.length_slider.configure(from_=3, to=6, number_of_steps=3)
                self.length_slider.set(3)
                self.update_slider_label(3)
            else:
                self.length_slider.configure(from_=8, to=25, number_of_steps=18)
                self.length_slider.set(8)
                self.update_slider_label(8)
        except Exception as e:
            print("le slide n'a pas été encore créé")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = PasswordApp()
    app.mainloop()
