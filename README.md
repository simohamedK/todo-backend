# Backend de Mon Projet To-Do List

## Description
Ce projet est l'API backend pour une application To-Do List. Il est développé en utilisant Flask et gère l'authentification des utilisateurs via JWT, ainsi que les opérations CRUD (création, récupération, mise à jour et suppression) sur les tâches.

## Fonctionnalités
- Authentification des utilisateurs avec JWT.
- Gestion des utilisateurs (création, récupération, mise à jour, suppression).
- Gestion des tâches (création, récupération, suppression, modification).
- API sécurisée pour interagir avec les tâches et utilisateurs.

## Installation

### Prérequis
- Python 3.x
- MySQL (ou autre base de données compatible)

### Backend
1. Clonez le dépôt :
    ```bash
    git clone https://github.com/simohamedK/todo-backend.git
    cd todo-backend
    ```

2. Créez un environnement virtuel et installez les dépendances :
    ```bash
    python -m venv venv
    source venv/bin/activate   # Sous Linux/macOS
    venv\Scripts\activate      # Sous Windows
    pip install -r requirements.txt
    ```

3. Configurez votre base de données MySQL et créez les tables nécessaires pour les utilisateurs, rôles et tâches. Vous devrez probablement ajuster la configuration de votre base de données dans le fichier `.env` ou un autre fichier de configuration.

4. Lancez l'application Flask :
    ```bash
    python app.py
    ```

   L'API sera accessible par défaut à `http://127.0.0.1:5000`.

## API Endpoints

### Authentification
- **POST /users/login**: Permet à un utilisateur de se connecter et d'obtenir un token JWT.

### Gestion des utilisateurs (Admin uniquement)
- **GET /users**: Récupérer tous les utilisateurs (admin uniquement).
- **GET /users/{id}**: Récupérer un utilisateur par son ID (admin uniquement).
- **POST /users**: Créer un nouvel utilisateur (admin uniquement).
- **PUT /users/{id}**: Mettre à jour un utilisateur (admin uniquement).
- **DELETE /users/{id}**: Supprimer un utilisateur (admin uniquement).

### Gestion des tâches
- **GET /tasks**: Récupérer toutes les tâches (utilisateur authentifié).
- **GET /tasks/{id}**: Récupérer une tâche par son ID (utilisateur authentifié).
- **POST /tasks**: Créer une nouvelle tâche (utilisateur authentifié).
- **PUT /tasks/{id}**: Mettre à jour une tâche (utilisateur authentifié).
- **DELETE /tasks/{id}**: Supprimer une tâche (utilisateur authentifié).

## Contribuer
1. Fork le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`).
3. Commitez vos modifications (`git commit -am 'Ajout de ma fonctionnalité'`).
4. Poussez vers votre fork (`git push origin feature/ma-fonctionnalite`).
5. Créez une pull request.
