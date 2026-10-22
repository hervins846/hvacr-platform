# Utilisation d'une image officielle Python légère
FROM python:3.11-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie et installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le code source du projet
COPY . .

# Commande de lancement par défaut de l'API FastAPI
CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]