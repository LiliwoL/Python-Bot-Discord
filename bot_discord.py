#!/usr/bin/python
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


# Creation du client Discord
# ############################################
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)


# Chemins vers les fichiers textes contenant les messages à envoyer
# ############################################
chemin_fichier = "./messages.txt"
chemin_fichier_tag_giphy = "./tag_giphy.txt"


# Clés API, Channel ID de discord et Token Discord chargés depuis le fichier .env
# ############################################
load_dotenv()

giphy_api_key = os.getenv('GIPHY_API_KEY')
discord_channel_id = os.getenv('DISCORD_CHANNEL_ID')
discord_TOKEN = os.getenv('DISCORD_TOKEN')


# Configuration du client GIPHY
# ############################################
configuration = giphy_client.Configuration()
configuration.api_key['api_key'] = giphy_api_key
api_instance = giphy_client.DefaultApi(giphy_client.ApiClient(configuration))


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

    # En fonction de ce qui est demandé, on appel la fonction de lecture
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

        # Envoi du message au groupe Discord
        channel = client.get_channel(discord_channel_id)
        if channel:
            try:
                await channel.send(embed=embed)
                print("Message envoyé au canal avec succès.")
            except discord.HTTPException as e:
                print("Erreur lors de l'envoi du message :", e)
            except discord.Forbidden:
                print("Permission refusée pour envoyer des messages dans le canal.")
        else:
            print("Impossible de trouver le canal avec l'ID :", discord_channel_id)

        # Attente d'une semaine (7 jours)
        await asyncio.sleep(10)


# Événement de démarrage du bot
@client.event
async def on_ready():
    print('Bot connecté en tant que', client.user.name)
    print('------')
    client.loop.create_task(envoyer_message())


# Démarrage du bot
client.run(discord_TOKEN)
