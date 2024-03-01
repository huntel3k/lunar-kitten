import disnake
from disnake.ext import commands

class ReverseText(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Odwraca podany tekst.')
    async def reverse(self, inter, text: str):
        if len(text) > 50:
            await inter.response.send_message('Twój tekst jest za długi! Ponieważ zawiera powyżej 50 znaków.', ephemeral=True)
        else:
            reversed_text = text[::-1]
            embed = disnake.Embed(
                title="Odwrócony tekst",
                description=f"Odwrócony tekst: {reversed_text}",
                color=6697881
            )

            await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(ReverseText(bot))
