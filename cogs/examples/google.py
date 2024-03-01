import disnake
from disnake.ext import commands

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='google', description='tak!')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self, inter):
        embed = disnake.Embed(
            title="boom",
            description=f"[google](https://google.com)",
            color=6697881
        )

        view = disnake.ui.View()
        button = disnake.ui.Button(
            style=disnake.ButtonStyle.secondary,
            emoji="<:chr_catANerd:1180166679725088798>",
            url="https://www.google.com/",
            label="Tak!"
        )
        view.add_item(button)

        await inter.response.send_message(embed=embed, view=view)


    @google.error
    async def google_error(self, inter, error):
        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(f"Jesteś na cooldownie! Spróbuj za {error.retry_after:.2f} sekund")

def setup(bot: commands.Bot):
    bot.add_cog(Test(bot))
