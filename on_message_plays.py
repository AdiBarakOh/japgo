import asyncio

async def alert_homework(message, client):
    
    REMINDER_SECONDS = 5760
    reminder_days = int(REMINDER_SECONDS // (24 * 60))
    
    if message.channel.name == "homework-help":
        await message.reply(content=f"Please react 👍 to this message when completed. I will remind you in {reminder_days} days.")
         
        def check_homework(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'
        
        try:
            await client.wait_for('reaction_add', timeout=REMINDER_SECONDS, check=check_homework)     
        except asyncio.TimeoutError:
            await message.channel.send('Did you forget your homework? 😢')
            await message.channel.send('you can still do it!')   
        else:
            await message.channel.send('お疲れ様! (おつかれさま)')
            

            
