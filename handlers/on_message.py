import asyncio
import logging
import sqlite3

import discord

from config import (
    BOT_PREFIX,
    DAYS_HOMEWORK_REMINDER,
    DISCORD_CLIENT,
    GRAMMER_CHANNEL_NAME,
    HOME_WORK_CHANNEL_NAME, 
    QUIZ_CHANNEL_NAME,
    WORDS_CHANNEL_NAME,
)
from services.database import add_grammer_to_db, add_word_to_db
from services.quiz import Quiz

client: discord.Client = DISCORD_CLIENT
logger = logging.getLogger('on_message')

async def alert_homework(message: discord.Message, client: discord.Client) -> None:
    if message.channel.name == HOME_WORK_CHANNEL_NAME:
        await message.reply(content=(
            f"""Please react 👍 to this message when completed.
            I will remind you in {DAYS_HOMEWORK_REMINDER} days."""
            ))
         
        def check_homework(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'
        
        try:
            await client.wait_for(
                'reaction_add',
                timeout=(DAYS_HOMEWORK_REMINDER * 24 * 60 * 60),
                check=check_homework,
            )     
        except asyncio.TimeoutError:
            await message.channel.send('Did you forget your homework? 😢')
            await message.channel.send('you can still do it!')   
        else:
            await message.channel.send('お疲れ様! (おつかれさま)')
            
async def add_words(message: discord.Message, client: discord.Client) -> None:
    if message.channel.name == WORDS_CHANNEL_NAME:
        try:
            if add_word_to_db(message.content):
                await message.channel.send(f'{message.content} was added to database.')
            else:
                await message.channel.send(
                    f'{message.content} was already in database. Do not waste my time!'
                )
        except sqlite3.ProgrammingError as adding_to_db:
                logger.info(adding_to_db)
                await message.channel.send(
                        f"""{message.content} was regected in our system for some unknown reason.
                        Maybe try to write the word another way?"""
                    ) 
                
async def add_grammer(message: discord.Message, client: discord.Client) -> None:
    if message.channel.name == GRAMMER_CHANNEL_NAME:
        try:
            add_grammer_to_db(message.content)
            await message.channel.send(f'{message.content} was added to database.')
        except sqlite3.ProgrammingError as adding_to_db:
            logger.info(adding_to_db)
            await message.channel.send(f'{message.content} was regected for some reason.')

def on_message_event() -> None:            
    @client.event
    async def on_message(message):
        logger.debug(
            f"{message.author} sent in {message.channel.name}: {message.content}"
        )
    
        message.content = message.content.lower()
        if message.author == client.user or BOT_PREFIX not in message.content:
            return
    
        message.content = message.content.replace(BOT_PREFIX, "")
        await alert_homework(message, client)
        await add_grammer(message, client)
        await add_words(message, client)
    
        if message.channel.name == QUIZ_CHANNEL_NAME:
            logger.debug("quiz should start")
            quiz: Quiz = Quiz(message, client)
            await quiz.main_quiz()










