import disnake
from disnake.ext import commands

# bot = commands.Bot()
# intents = disnake.Intents.default()
# intents.members = True

class WelcomeGoodbyeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(f"Cog dla powitan i pozegnan dziala!")
    #
    #
    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     # Replace 'your-welcome-channel-id' with the actual ID of your welcome channel
    #     welcome_channel = bot.get_channel(1194589048912744448)
    #     if welcome_channel:
    #         await welcome_channel.send(f"Welcome, {member.mention}! Enjoy your stay.")
    #
    #
    # @commands.Cog.listener()
    # async def on_member_remove(self, member):
    #     # Replace 'your-goodbye-channel-id' with the actual ID of your goodbye channel
    #     goodbye_channel = bot.get_channel(1194589048912744448)
    #     if goodbye_channel:
    #         await goodbye_channel.send(f"Goodbye, {member.name}! We'll miss you.")


def setup(bot):
    bot.add_cog(WelcomeGoodbyeCog(bot))
