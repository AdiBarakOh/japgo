import asyncio
import discord
import logging
import sqlite3


from data.database import add_grammer_to_db, add_word_to_db


logger = logging.getLogger('on_message')

async def alert_homework(message: discord.Message, client: discord.Client) -> None:
    REMINDER_SECONDS = 5760
    reminder_days = int(REMINDER_SECONDS // (24 * 60))
    if message.channel.name == "homework-help":
        await message.reply(content=(
            f"""Please react 👍 to this message when completed.
            I will remind you in {reminder_days} days."""
            ))
         
        def check_homework(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'
        
        try:
            await client.wait_for('reaction_add', timeout=REMINDER_SECONDS, check=check_homework)     
        except asyncio.TimeoutError:
            await message.channel.send('Did you forget your homework? 😢')
            await message.channel.send('you can still do it!')   
        else:
            await message.channel.send('お疲れ様! (おつかれさま)')
            
async def add_words(message: discord.Message, client: discord.Client) -> None:
    if message.channel.name == "words-kanji":
        try:
            if add_word_to_db(message.content):
                await message.channel.send(f'{message.content} was added to database.')
            else:
                await message.channel.send(f'{message.content} was already in database. Do not waste my time!')
        except sqlite3.ProgrammingError as adding_to_db:
                logger.info(adding_to_db)
                await message.channel.send(
                        f"""{message.content} was regected in our system for some unknown reason.
                        Maybe try to write the word another way?"""
                    ) 
                
async def add_grammer(message: discord.Message, client: discord.Client) -> None:
    if message.channel.name == "grammer":
        try:
            add_grammer_to_db(message.content)
            await message.channel.send(f'{message.content} was added to database.')
        except sqlite3.ProgrammingError as adding_to_db:
            logger.info(adding_to_db)
            await message.channel.send(f'{message.content} was regected for some reason.')
            

        

            
    
                    
        
                
                
                  
            
