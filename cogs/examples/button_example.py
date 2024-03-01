import disnake
from disnake.ext import commands


class Buttons(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='button_test', description='Test przycisków!')
    async def buttons(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(
            "Potrzebujesz pomocy?",
            components=[
                disnake.ui.Button(label="Tak", style=disnake.ButtonStyle.success, custom_id="yes"),
                disnake.ui.Button(label="Nie", style=disnake.ButtonStyle.danger, custom_id="no"),
                disnake.ui.Button(label="Przyciski", style=disnake.ButtonStyle.url, url="https://guide.disnake.dev/interactions/buttons"),
                disnake.ui.Button(emoji="<:chr_catANerd:1180166679725088798>", style=disnake.ButtonStyle.secondary, custom_id="cat_nerd")
            ],
        )

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["yes", "no", "link", "cat_nerd"]:
            return

        if inter.component.custom_id == "yes":
            await inter.response.send_message("Skontaktuj się z nami: https://discord.gg/YmVf6Sd!")
        elif inter.component.custom_id == "no":
            await inter.response.send_message("Zrozumiano!")
        elif inter.component.custom_id == "link":
            await inter.response.send_message("https://guide.disnake.dev/interactions/buttons")
        elif inter.component.custom_id == "cat_nerd":
            await inter.response.send_message("um akshually! :nerd:")

def setup(bot: commands.Bot):
    bot.add_cog(Buttons(bot))
