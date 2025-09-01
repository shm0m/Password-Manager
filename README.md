# Password Manager

Un gestionnaire de mots de passe simple en Python qui permet de stocker, chiffrer et récupérer vos mots de passe de façon sécurisée.

## Fonctionnalités

- Ajout de mots de passe pour différents sites
- Récupération des mots de passe enregistrés
- Liste des sites enregistrés
- Chiffrement des mots de passe avec une clé dérivée d’un mot de passe maître
- Interface en ligne de commande interactive

## Prérequis

- Python 3.13
- MySQL Server
- Les modules suivants :
  - `mysql-connector-python`
  - `cryptography`
  - `rich`

## Installation

1. Clonez le dépôt :
   ```sh
   git clone <url-du-repo>
   cd Password-Manager
   ```

2. Installez les dépendances :
   ```sh
   pip install mysql-connector-python cryptography rich
   ```

3. Configurez votre base MySQL :
   - Créez une base de données nommée `password_manager`
   - Modifiez les paramètres de connexion dans [`secure.py`](secure.py) si besoin

## Utilisation

Lancez le script principal :
```sh
python secure.py
```

Suivez les instructions à l’écran pour ajouter, récupérer ou lister vos mots de passe.

## Sécurité

- Les mots de passe sont chiffrés avec Fernet (AES) avant d’être stockés en base.
- Le mot de passe maître est utilisé pour dériver la clé de chiffrement.
- Ne partagez jamais votre mot de passe maître.

## Auteur

Shaima DEROUICH 

