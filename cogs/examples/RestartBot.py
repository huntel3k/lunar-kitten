import disnake
from disnake.ext import commands

class RestartBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Restartuje bota.")
    async def restart(self, inter):
        embed = disnake.Embed(
            title="Restartowanie bota",
            description=f"Restartowanie...",
            color=5420608
        )
        await inter.response.send_message(embed=embed)
        await self.bot.close()
def setup(bot: commands.Bot):
    bot.add_cog(RestartBot(bot))