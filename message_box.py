import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

# Configuration du mode sombre
ctk.set_appearance_mode("dark")  # Active le mode sombre
ctk.set_default_color_theme("dark-blue")  # Thème de couleur par défaut pour customtkinter

# Couleurs pour le bouton
fg_color_button = "#931cff"
hover_color_button = "#6b00b3"

# Fonction pour confirmer le retour
def confirm_return():
    # Affiche la boîte de message de confirmation
    response = CTkMessagebox(
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

# Configuration de la fenêtre principale
app = ctk.CTk()
app.geometry("300x200")
app.title("Application avec retour")

# Bouton "Retour" avec appel de la fonction de confirmation
return_button = ctk.CTkButton(
    app,
    text="Retour",
    fg_color=fg_color_button,
    hover_color=hover_color_button,
    command=confirm_return
)
return_button.pack(pady=20)

app.mainloop()
