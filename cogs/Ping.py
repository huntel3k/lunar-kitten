import disnake
from disnake.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='ping', description='Podaje opóźnienie bota!')
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Pong! 🏓",
            description=f"Opóźnienie: {round(self.bot.latency * 1000)}ms",
            color=6697881
        )

        await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
