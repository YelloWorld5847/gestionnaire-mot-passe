# Application de Gestion de Comptes et de Mots de Passe

Cette application gère les comptes d'utilisateurs et leurs mots de passe, offrant des fonctionnalités de connexion sécurisée, de gestion des mots de passe, de chiffrement des données sensibles et d'un générateur avancé de mots de passe.

---

## Fonctionnalités principales

### Gestion des utilisateurs
- **Connexion sécurisée** : Authentification par mot de passe haché (bcrypt) avec utilisation de sel.
- **Création de comptes** : Possibilité de créer un nouveau compte via l'interface.
- **Hachage et stockage** : Les mots de passe utilisateurs sont protégés par un hachage robuste.

### Gestion des mots de passe
- **Chiffrement des données** : Utilisation de la bibliothèque `Fernet` pour chiffrer et déchiffrer les mots de passe stockés.
- **Ajout et modification de mots de passe** : Enregistrement de nouveaux mots de passe ou mise à jour des mots de passe existants.
- **Recherche et affichage** : Fonction de recherche pour retrouver rapidement des mots de passe spécifiques.
- **Génération de mots de passe** :
  - Aléatoires
  - Mémorables
  - Codes PIN

### Générateur de mots de passe intégré
Le générateur propose trois modes :
1. **Aléatoire** :
   - Combinaison de lettres (minuscules et majuscules), chiffres et symboles.
   - Longueur configurable (8 à 25 caractères).
   - Activation/désactivation des symboles et chiffres.

2. **Mémorable** :
   - Génération de mots ou de phrases faciles à mémoriser.
   - Les mots sont séparés par des tirets (exemple : *arbre-chat-lune*).
   - Longueur configurable (3 à 6 mots).

3. **Code PIN** :
   - Génération de codes numériques (de 3 à 20 chiffres).

---

## Installation

### 1. Prérequis
- **Python 3.10 ou supérieur**
- **Bibliothèques nécessaires** :
  - `bcrypt`
  - `sqlite3` (intégré à Python)
  - `cryptography`
  - `customtkinter`
  - `CTkMessagebox`

Installez les dépendances avec :
```bash
pip install bcrypt cryptography customtkinter ctkmessagebox
