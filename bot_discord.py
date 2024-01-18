#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Imports nécessaires
# ############################################
import discord
import random
import asyncio
import giphy_client
from giphy_client.rest import ApiException
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Chargement du fichier .env
load_dotenv()


# Creation du client Discord
# ############################################
intents                     = discord.Intents.default()
intents.typing              = False
intents.presences           = False
client                      = discord.Client(intents=intents)


# Chemins vers les fichiers textes contenant les messages à envoyer
# ############################################
chemin_fichier              = "./messages.txt"
chemin_fichier_tag_giphy    = "./tag_giphy.txt"


# Définit la date maximale (à partir de laquelle le programme devra s'arrêter de lui même)
# ############################################
# Date définie dans le fichier .env
max_date_year               = int(os.getenv('MAX_DATE_YEAR'))   # On doit impérativement avoir un INT
max_date_month              = int(os.getenv('MAX_DATE_MONTH'))
max_date_day                = int(os.getenv('MAX_DATE_DAY'))
maximal_date                = datetime(max_date_year, max_date_month, max_date_day)  # Remplacez avec votre date maximale


# Délai entre 2 envois défini dans le fichier .env
delay                       = float(os.getenv('DELAY'))


# Clés API, Channel ID de discord et Token Discord chargés depuis le fichier .env
# ############################################

giphy_api_key               = os.getenv('GIPHY_API_KEY')
discord_channel_ids         = os.getenv('DISCORD_CHANNEL_IDS').split(',')   # On doit impérativement avoir un dict contenant des ints
discord_TOKEN               = os.getenv('DISCORD_TOKEN')


# Configuration du client GIPHY
# ############################################
configuration               = giphy_client.Configuration()
configuration.api_key['api_key'] = giphy_api_key
api_instance                = giphy_client.DefaultApi(giphy_client.ApiClient(configuration))


# Fonction pour lire les messages à partir du fichier texte
def lire_messages(messages_type):

    # Choix du fichier à lire en fonction du type
    if messages_type == "discord":
        chemin = chemin_fichier
    elif messages_type == "giphy":
        chemin = chemin_fichier_tag_giphy

    with open(chemin, "r") as f:
        messages = f.readlines()
    return [msg.strip() for msg in messages]


# Fonction pour choisir un message aléatoire
def choisir_message(messages_type):

    # En fonction de ce qui est demandé, on appelle la fonction de lecture
    messages = lire_messages(messages_type)
    return random.choice(messages)


# Fonction pour rechercher un GIF avec l'API GIPHY
def rechercher_gif(requete):
    try:
        api_instance = giphy_client.DefaultApi()

        # https://github.com/Giphy/giphy-python-client/blob/master/docs/DefaultApi.md#gifs_search_get
        response = api_instance.gifs_search_get(
            api_key=giphy_api_key,
            q=requete,
            rating='pg-13',
            limit=1)
        if response.data:
            gifs = response.data
            if gifs:
                gif_url = gifs[0].images.original.url
                return gif_url

        print("Aucun GIF trouvé pour la requête :", requete)
        return None
    except ApiException as e:
        print("Exception lors de la recherche du GIF :", e)
        return None


# Fonction pour envoyer le message avec un GIF chaque semaine
async def envoyer_message():
    # Si la date maximale est atteinte, le programme s'arrête
    while datetime.now() <= maximal_date:
        await client.wait_until_ready()
        while not client.is_closed():
            # Choix du message
            message = choisir_message("discord")

            # Recherche d'un GIF aléatoire
            gif_requete = choisir_message("giphy")
            gif_url = rechercher_gif(gif_requete)

            print("Image trouvée: ", gif_url)

            # Création de l'embed Discord
            embed = discord.Embed(description=message)
            embed.set_image(url=gif_url)

            # Envoi du message aux groupes Discord
            for channel_id in discord_channel_ids:
                channel = client.get_channel( int(channel_id) )
                # Votre code pour envoyer le message dans le channel spécifié
                if channel:
                    try:
                        await channel.send(embed=embed)
                        print("Message envoyé au canal avec succès.")
                    except discord.HTTPException as e:
                        print("Erreur lors de l'envoi du message :", e)
                    except discord.Forbidden:
                        print("Permission refusée pour envoyer des messages dans le canal.")
                else:
                    print("Impossible de trouver le canal avec l'ID :", channel_id)

            # Attente d'un délai avant le prochain envoi (durée définie dans le .env)
            await asyncio.sleep(delay)

    # Une fois que la date maximale est atteinte, arrêter le programme
    print("Date maximale atteinte. Arrêt du programme.")
    await client.close()


# Événement de démarrage du bot
@client.event
async def on_ready():
    print('Bot connecté en tant que', client.user.name)
    print('------')
    client.loop.create_task(envoyer_message())


# Démarrage du bot
client.run(discord_TOKEN)
