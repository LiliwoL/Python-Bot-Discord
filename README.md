# Bot Discord pour rappeler aux stagiaires de publier un rapport de stage hebdomadaire sur la plateforme Moodle

# Objectif

Développer un Bot Discord en Python pour rappeler chaque fin de semaine de publier son rapport de stage.

# Installation

Dépendances:

```bash
pip install -r requirements.txt
```

Programme:
```bash
python3 bot_discord.py
```

# Configuration

Créer le fichier **.env** avec vos valeurs.

A configurer:
```dotenv
# Variables d'environnement à remplir avant!
GIPHY_API_KEY=

# Liste des IDs des salons séparés par des virgules et entre crochets
DISCORD_CHANNEL_IDS="00000000,11111111"

# Token de l'application
DISCORD_TOKEN=

# Date à laquelle le script ,du bot doit s'arrêter
MAX_DATE_YEAR=
# Ne pas mettre le 0 pour les mois avant octobre
MAX_DATE_MONTH=
MAX_DATE_DAY=

# Délai entre 2 envois en secondes (ici 7 jours)
#DELAY=604800     # "7 * 24 * 60 * 60"
DELAY=
```

# Sources

ChatGPT!
https://www.commentcoder.com/bot-discord-python/


# Utiliser des fichiers d'environnement dans Python

https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1