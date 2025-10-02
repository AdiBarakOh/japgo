import os
TOKEN = os.getenv("DISCORD_TOKEN")
print("TOKEN is:", TOKEN is not None)  # should print True