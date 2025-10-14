import logging
import os

import discord

from data_bases import create_db
from on_message_plays import add_grammer, add_words, alert_homework
from quizes import Quiz

logging.basicConfig(filename='main_log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger('main')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

create_db()

@client.event
async def on_message(message):
    logger.debug(
        f"{message.author} sent in {message.channel.name}: {message.content}"
        )
    
    message.content = message.content.lower()
    if message.author == client.user:
        return
    
    await alert_homework(message, client)
    await add_grammer(message, client)
    await add_words(message, client)
    
    if message.channel.name == "quiz" and "quiz" in message.content:
        quiz = Quiz(message, client)
        await quiz.main_quiz()    
        
        
DISCORD_TOKEN = os.getenv("JAPGO_DISCORD_TOKEN") # Requires token as an env variable
client.run(DISCORD_TOKEN)

