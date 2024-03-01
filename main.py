from dotenv import load_dotenv
from disnake.ext import commands
import os
import disnake


intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

load_dotenv("secret.env")
token = os.getenv("TOKEN")

@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.idle)
    print(f"\033[91m|------------------------------|")
    print(f"\033[91m| \033[92mOnline! \033[96mbot: \033[93m{bot.user.name} 🐱 \033[91m|")
    print(f"\033[91m|------------------------------|")

bot.load_extension('cogs.MiniGames')
bot.load_extension('cogs.Info')
bot.load_extension('cogs.Ping')
bot.load_extension('cogs.Moderation')
bot.load_extension('cogs.VoteSystem')

bot.run(token)
