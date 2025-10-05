
import os

import discord

from on_message_plays import alert_homework

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == client.user:
        return
    
    await alert_homework(message, client)
    
    



DISCORD_TOKEN = os.getenv("JAPGO_DISCORD_TOKEN") # Requires token as an env variable
client.run(DISCORD_TOKEN)

