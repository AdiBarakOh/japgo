import logging

import discord

from config import DISCORD_CLIENT, DISCORD_TOKEN
from handlers import on_message
from services.database import create_db

logging.basicConfig(filename='main_log.log', encoding='utf-8', level=logging.DEBUG)

logger = logging.getLogger('main')

client: discord.Client = DISCORD_CLIENT

create_db()
on_message.on_message_event()

client.run(DISCORD_TOKEN)

