import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path='token.env')

intents = disnake.Intents.all()

activity = disnake.Activity(type=disnake.ActivityType.watching, name="dev")

bot = commands.InteractionBot(intents=intents, activity=activity, status=disnake.Status.idle)


@bot.event
async def on_ready():
    print("}------✅------{")
    print("}  bocik zyje  {")
    print("}------✅------{")


bot.load_extension("cogs.moderation")
bot.load_extension("cogs.Utilities")
bot.load_extension("cogs.LoggingSystem")

token = os.getenv('TOKEN')
bot.run(token)
