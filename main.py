import logging

import discord

from config import DISCORD_CLIENT, DISCORD_TOKEN
from data.database import create_db
from handlers import on_message

logger = logging.getLogger('main')

client: discord.Client = DISCORD_CLIENT

create_db()


client.run(DISCORD_TOKEN)

