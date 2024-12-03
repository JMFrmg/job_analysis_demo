FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Copier le fichier requirements.txt dans le répertoire de travail
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Définir la commande pour lancer l'application
CMD ["python", "app.py"]